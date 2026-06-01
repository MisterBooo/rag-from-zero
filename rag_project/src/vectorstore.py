"""向量库模块 —— ChromaDB 本地封装,对应文章第 5 章(检索召回)的存储侧。

负责把 chunk 的向量存起来、按相似度查回来。用 ChromaDB 本地持久化,
零运维、clone 即用。对应文章:https://www.wsxdmx.com/projects/rag-system/c/05-retrieval
"""

from pathlib import Path

from .chunker import Chunk


class VectorStore:
    """ChromaDB 向量库封装。chromadb 惰性导入,仅 import 本模块不需要装它。"""

    def __init__(self, persist_dir: Path, collection: str = "rag_docs") -> None:
        """打开 / 新建一个持久化的向量集合。

        Args:
            persist_dir: 本地持久化目录
            collection: 集合名
        """
        import chromadb  # 惰性导入

        self._client = chromadb.PersistentClient(path=str(persist_dir))
        # 关掉 chroma 自带的 embedding(我们自己用 bge-m3 算好向量再传进来)
        self._col = self._client.get_or_create_collection(
            name=collection, metadata={"hnsw:space": "cosine"}
        )

    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        """把 chunk 及其向量写入库中。

        Args:
            chunks: 文本块列表
            embeddings: 与 chunks 一一对应的向量
        """
        if not chunks:
            return
        ids = [f"{c.source}#{c.chunk_id}" for c in chunks]  # 来源+序号,稳定且可去重
        self._col.add(
            ids=ids,
            embeddings=embeddings,
            documents=[c.text for c in chunks],
            metadatas=[{"source": c.source, "chunk_id": c.chunk_id} for c in chunks],
        )

    def query(self, query_embedding: list[float], top_k: int = 5) -> list[Chunk]:
        """按向量相似度取回最相关的若干 chunk。

        Args:
            query_embedding: 查询向量
            top_k: 返回数量

        Returns:
            相似度从高到低的 Chunk 列表
        """
        res = self._col.query(query_embeddings=[query_embedding], n_results=top_k)
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        return [
            Chunk(text=d, source=m.get("source", ""), chunk_id=int(m.get("chunk_id", 0)), metadata=dict(m))
            for d, m in zip(docs, metas)
        ]

    def all_chunks(self) -> list[Chunk]:
        """取出库里所有 chunk(BM25 路要在内存重建倒排,需要全量文本)。"""
        res = self._col.get(include=["documents", "metadatas"])
        docs = res.get("documents", []) or []
        metas = res.get("metadatas", []) or []
        return [
            Chunk(text=d, source=m.get("source", ""), chunk_id=int(m.get("chunk_id", 0)), metadata=dict(m))
            for d, m in zip(docs, metas)
        ]

    def count(self) -> int:
        """返回库中已有的 chunk 数量(建库后做健康检查用)。"""
        return self._col.count()
