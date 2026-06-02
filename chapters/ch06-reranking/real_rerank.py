"""
RAG 教程第 6 章 - 真实精排(用开源 Cross-Encoder)

需要装库(macOS / Linux):pip3 install sentence-transformers
        (Windows:pip install sentence-transformers)
首次运行会自动下载模型权重,需要联网。

和玩具粗排对比:这里「保险责任」(真正回答了"能不能赔")会被排到第一,
因为 Cross-Encoder 把 query 和 doc 拼在一起、读懂了它们的关系。

对应文章:https://www.wsxdmx.com/projects/rag-system/c/06-reranking
"""
import sys

try:
    from sentence_transformers import CrossEncoder
except ImportError as e:
    print(f"❌ 缺少依赖({e.name}),装好再跑:")
    print("  macOS / Linux:  pip3 install sentence-transformers")
    print("  Windows:        pip install sentence-transformers")
    print("  pypi 慢:        pip3 install sentence-transformers -i https://pypi.tuna.tsinghua.edu.cn/simple")
    sys.exit(1)

# 开源中文 reranker;按需替换为 bge-reranker-large / MiniLM-cross / gte-reranker
reranker = CrossEncoder("BAAI/bge-reranker-base")


def rerank(query, candidates, top_k=5):
    pairs = [(query, doc) for doc in candidates]  # 每个候选与 query 组成一对
    scores = reranker.predict(pairs)  # Cross-Encoder 逐对打相关性分
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]


def rerank_batch(query, coarse_candidates, rerank_n=10, top_k=5):
    """工程提速:① 只精排前 rerank_n 个候选;② 一次性批量推理。"""
    candidates = coarse_candidates[:rerank_n]
    pairs = [(query, doc) for doc in candidates]
    scores = reranker.predict(pairs, batch_size=32)  # 批大小按显存调
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in ranked[:top_k]]


if __name__ == "__main__":
    query = "孩子摔伤住院,意外险能赔吗?"
    candidates = [
        "第2条 保险责任:本保险承保意外伤害导致的医疗费用,予以赔付",
        "第3条 责任免除:孩子在学校受伤住院,属下列情形之一的不予赔付",
    ]
    for doc, score in rerank(query, candidates):
        print(f"  {score:.3f}  {doc}")
    # 这次「保险责任」会排第一——精排读懂了 query 和 doc 的关系。
