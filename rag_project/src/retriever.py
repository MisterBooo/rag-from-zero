"""检索模块 —— 对应文章第 5 章(检索召回)。

向量检索擅长「意思相近」,BM25 擅长「关键词精确命中」,两者互补。
本模块做双路检索 + 融合(RRF),既能查到同义改写,也不漏专有名词。
RRF(Reciprocal Rank Fusion)只看排名不看分数,天然绕开「两套分数量纲不同」的麻烦。
对应文章:https://www.wsxdmx.com/projects/rag-system/c/05-retrieval
"""

import math
import re
from dataclasses import dataclass

from .chunker import Chunk
from .embedder import Embedder
from .vectorstore import VectorStore


@dataclass
class RetrievedChunk:
    """检索结果:一个 chunk 加上它的相关性得分(这里是 RRF 融合分)。"""

    chunk: Chunk
    score: float


def _tokenize(text: str) -> list[str]:
    """分词:优先用 jieba(词级,更准);没装就退到字级。两者都能让 BM25 跑起来。"""
    try:
        import jieba  # 可选依赖

        return [t for t in jieba.lcut(text) if t.strip()]
    except Exception:
        return [ch for ch in re.sub(r"\s", "", text)]  # 字级兜底


class _BM25:
    """最小可用的 BM25 实现(对应第 5 章手写的那段,工程化一点)。"""

    def __init__(self, docs_tokens: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.docs = docs_tokens
        self.N = len(docs_tokens)
        self.avgdl = sum(len(d) for d in docs_tokens) / self.N if self.N else 0.0
        self.df: dict[str, int] = {}
        for d in docs_tokens:
            for t in set(d):
                self.df[t] = self.df.get(t, 0) + 1

    def _idf(self, t: str) -> float:
        n = self.df.get(t, 0)
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def scores(self, query: str) -> list[float]:
        q = _tokenize(query)
        out = []
        for doc in self.docs:
            score, dl = 0.0, len(doc)
            for t in q:
                f = doc.count(t)
                if not f:
                    continue
                tf = f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / (self.avgdl or 1)))
                score += self._idf(t) * tf
            out.append(score)
        return out


class Retriever:
    """向量 + BM25 双路混合检索器。"""

    def __init__(self, store: VectorStore, embedder: Embedder, chunks: list[Chunk]) -> None:
        """初始化检索器。

        Args:
            store: 已建好索引的向量库(向量路)
            embedder: 查询向量化器(向量路)
            chunks: 全部 chunk(BM25 路在内存里建倒排)
        """
        self.store = store
        self.embedder = embedder
        self.chunks = chunks
        self._bm25 = _BM25([_tokenize(c.text) for c in chunks]) if chunks else None

    @staticmethod
    def _key(c: Chunk) -> str:
        return f"{c.source}#{c.chunk_id}"

    def retrieve(self, query: str, top_k: int = 5, top_n: int = 20, rrf_k: int = 60) -> list[RetrievedChunk]:
        """混合检索:两路各取 top_n 候选,再用 RRF 融合,返回 top_k。

        Args:
            query: 用户查询
            top_k: 最终返回数量
            top_n: 每路召回的候选数(候选池越大召回上限越高)
            rrf_k: RRF 常数,经验值 60

        Returns:
            融合排序后的 RetrievedChunk 列表
        """
        ranked_lists: list[list[Chunk]] = []

        # 向量路(库为空 / 没装 embedding 模型时自动跳过,不至于崩)
        try:
            qv = self.embedder.encode_query(query)
            ranked_lists.append(self.store.query(qv, top_k=top_n))
        except Exception:
            pass

        # BM25 路
        if self._bm25 is not None:
            scores = self._bm25.scores(query)
            order = sorted(range(len(self.chunks)), key=lambda i: scores[i], reverse=True)
            ranked_lists.append([self.chunks[i] for i in order[:top_n] if scores[i] > 0])

        # RRF 融合:每个 chunk 在每个排名表里贡献 1/(rrf_k + 名次)
        fused: dict[str, float] = {}
        by_key: dict[str, Chunk] = {}
        for lst in ranked_lists:
            for rank, c in enumerate(lst, start=1):
                k = self._key(c)
                fused[k] = fused.get(k, 0.0) + 1.0 / (rrf_k + rank)
                by_key.setdefault(k, c)

        ordered = sorted(fused.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
        return [RetrievedChunk(chunk=by_key[k], score=s) for k, s in ordered]
