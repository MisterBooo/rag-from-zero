"""
RAG 教程第 4 章 - 玩具版"向量化"(零依赖)

不需要装任何库,直接 python3 toy_embedding.py 就能跑。
目的:先用最朴素的"字级词袋向量 + 余弦相似度"理解"文字→向量→算距离",
再亲眼看到它的硬伤——不懂近义词,从而明白为什么要用"学出来的"Embedding。

对应文章:https://www.wsxdmx.com/projects/rag-system/c/04-embedding
"""
import math


def to_vector(text: str) -> dict:
    """玩具向量:统计每个字出现的次数(字级词袋)。真实用 BGE 等模型输出稠密向量。"""
    v = {}
    for ch in text:
        v[ch] = v.get(ch, 0) + 1
    return v


def cosine(a: dict, b: dict) -> float:
    """余弦相似度:两个向量夹角的接近程度,1 最像、0 完全不像。"""
    dot = sum(cnt * b.get(ch, 0) for ch, cnt in a.items())
    na = math.sqrt(sum(c * c for c in a.values()))
    nb = math.sqrt(sum(c * c for c in b.values()))
    return dot / (na * nb) if na and nb else 0.0


if __name__ == "__main__":
    query = "保险理赔"
    docs = ["理赔流程说明", "索赔方法介绍", "等待期是多久"]
    qv = to_vector(query)
    print(f"query = {query}\n")
    for d in docs:
        print(f"  cos={cosine(qv, to_vector(d)):.2f}  {d}")

    print("\n注意:'索赔方法'和'理赔'是一个意思,却因为字面不同得了低分。")
    print("这就是词袋的硬伤——只懂字面,不懂意思。真实 Embedding 能解决它。")
