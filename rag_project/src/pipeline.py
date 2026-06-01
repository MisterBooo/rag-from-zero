"""主流程 —— 把 loader → chunker → embedder → vectorstore → retriever →
reranker → query_processor → generator 串成一条完整链路。

这是整个项目的「装配车间」:上面每个模块单独看是一个零件,这里把它们拼成
一台能从「一个问题」走到「一段带出处的答案」的机器。

scripts/build_index.py 调 build_index() 离线建库;scripts/ask.py 调 ask() 在线问答。
"""

from pathlib import Path

from . import config
from .chunker import chunk_doc
from .embedder import Embedder
from .generator import Answer, generate
from .loader import load_dir
from .query_processor import process_query
from .reranker import Reranker
from .retriever import RetrievedChunk, Retriever
from .vectorstore import VectorStore


class RAGPipeline:
    """端到端 RAG 流程。建库一次,之后反复 ask。"""

    def __init__(self, persist_dir: Path | None = None) -> None:
        """装配各模块(连接向量库;模型按需惰性加载)。

        Args:
            persist_dir: 向量库持久化目录(默认取 config.CHROMA_DIR)
        """
        self.persist_dir = Path(persist_dir or config.CHROMA_DIR)
        self.embedder = Embedder(config.EMBEDDING_MODEL)
        self.store = VectorStore(self.persist_dir)
        self.reranker = Reranker(config.RERANKER_MODEL) if config.USE_RERANK else None
        self._refresh_retriever()

    def _refresh_retriever(self) -> None:
        """(重)从向量库加载全部 chunk,重建检索器(BM25 路需要全量文本)。"""
        chunks = self.store.all_chunks()
        self.retriever = Retriever(self.store, self.embedder, chunks)

    def build_index(self, docs_dir: Path | None = None) -> int:
        """离线建库:加载 → 切分 → 向量化 → 入库。

        Args:
            docs_dir: 文档目录(默认 config.DATA_DIR)

        Returns:
            本次入库的 chunk 总数
        """
        docs = load_dir(Path(docs_dir or config.DATA_DIR))
        all_chunks = []
        for doc in docs:
            all_chunks.extend(chunk_doc(doc, config.CHUNK_SIZE, config.CHUNK_OVERLAP))
        if all_chunks:
            embeddings = self.embedder.encode([c.text for c in all_chunks])
            self.store.add(all_chunks, embeddings)
        self._refresh_retriever()  # 让新入库的 chunk 立刻对 BM25 路可见
        return len(all_chunks)

    def ask(self, query: str) -> Answer:
        """在线问答:查询改写 → 双路检索(含扩展)→ 重排 → 带引用生成。

        Args:
            query: 用户问题

        Returns:
            Answer:带引用的答案
        """
        pq = process_query(query)

        # 用「改写 + 扩展」的多个查询各召回一批,按 chunk 去重合并成候选池
        pool: dict[str, RetrievedChunk] = {}
        for q in pq.all_queries()[:3]:
            for rc in self.retriever.retrieve(q, top_k=config.RETRIEVE_TOP_N, top_n=config.RETRIEVE_TOP_N):
                key = f"{rc.chunk.source}#{rc.chunk.chunk_id}"
                if key not in pool or rc.score > pool[key].score:
                    pool[key] = rc
        candidates = sorted(pool.values(), key=lambda rc: rc.score, reverse=True)

        # 重排(用原始问题精排);没开重排就直接取候选池前 K
        if self.reranker is not None and candidates:
            contexts = self.reranker.rerank(query, candidates, top_k=config.RERANK_TOP_K)
        else:
            contexts = candidates[: config.RERANK_TOP_K]

        return generate(query, contexts)
