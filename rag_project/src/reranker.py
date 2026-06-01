"""重排模块 —— 对应文章第 6 章(重排与检索优化)。

检索召回讲究「快而广」,难免混进不相关的块。重排用更重的 cross-encoder
模型对候选逐一精算相关性,把真正相关的顶到前面,再喂给 LLM。
对应文章:https://www.wsxdmx.com/projects/rag-system/c/06-reranking
"""

from .retriever import RetrievedChunk


class Reranker:
    """基于 cross-encoder 的重排器。模型惰性加载,仅 import 不触发下载。"""

    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3") -> None:
        """记录模型名;真正加载推迟到第一次 rerank。

        Args:
            model_name: cross-encoder 重排模型名
        """
        self.model_name = model_name
        self._model = None

    def _ensure_model(self):
        if self._model is None:
            from sentence_transformers import CrossEncoder  # 惰性导入

            self._model = CrossEncoder(self.model_name)
        return self._model

    def rerank(self, query: str, candidates: list[RetrievedChunk], top_k: int = 5) -> list[RetrievedChunk]:
        """对候选 chunk 重新打分排序。

        Args:
            query: 用户查询
            candidates: 检索阶段召回的候选
            top_k: 重排后保留数量

        Returns:
            按重排得分从高到低的 RetrievedChunk 列表
        """
        if not candidates:
            return []
        model = self._ensure_model()
        # 批量推理:把 (query, doc) 对一次性喂进去,而不是 for 循环逐条(第 6 章提速第一招)
        pairs = [(query, rc.chunk.text) for rc in candidates]
        scores = model.predict(pairs)
        reranked = [RetrievedChunk(chunk=rc.chunk, score=float(s)) for rc, s in zip(candidates, scores)]
        reranked.sort(key=lambda rc: rc.score, reverse=True)
        return reranked[:top_k]
