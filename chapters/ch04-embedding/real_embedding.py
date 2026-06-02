"""
RAG 教程第 4 章 - 真实 Embedding(用开源 BGE)

需要装库(macOS / Linux):pip3 install sentence-transformers
        (Windows:pip install sentence-transformers)
首次运行会自动下载模型权重(几百 MB),需要联网。

和玩具版对比:这里 "索赔方法" 会和 "理赔流程" 一样拿到高分,因为模型学过它们语义相近。

对应文章:https://www.wsxdmx.com/projects/rag-system/c/04-embedding
"""
import sys

try:
    from sentence_transformers import SentenceTransformer, util
except ImportError as e:
    print(f"❌ 缺少依赖({e.name}),装好再跑:")
    print("  macOS / Linux:  pip3 install sentence-transformers")
    print("  Windows:        pip install sentence-transformers")
    print("  pypi 慢:        pip3 install sentence-transformers -i https://pypi.tuna.tsinghua.edu.cn/simple")
    sys.exit(1)

# 中文场景常用的开源模型;按需换成 bge-large-zh / gte / e5 等(见正文选型表)
model = SentenceTransformer("BAAI/bge-base-zh-v1.5")


def search(query, docs, top_k=3):
    q = model.encode(query, normalize_embeddings=True)
    d = model.encode(docs, normalize_embeddings=True)
    scores = util.cos_sim(q, d)[0]
    ranked = sorted(zip(docs, scores.tolist()), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]


if __name__ == "__main__":
    query = "保险理赔"
    docs = ["理赔流程说明", "索赔方法介绍", "等待期是多久"]
    for doc, score in search(query, docs):
        print(f"  cos={score:.2f}  {doc}")
    # "索赔方法" 这次也会拿到高分——学习得到的向量懂"意思"。
