"""
RAG 教程第 5 章 - 纯 Python 实现 BM25(零依赖)

不需要装任何库,直接 python bm25_demo.py 就能跑。
目的:亲手实现关键词检索的标准算法 BM25,看它怎么"精确命中术语",
也看清它的硬伤——不懂近义词。这正是后面要叠加向量检索做"混合检索"的原因。

对应文章:https://www.wsxdmx.com/projects/rag-system/c/05-retrieval
"""
import math
import re

docs = [
    "等待期说明:本产品等待期为90天,等待期内出险不予赔付",
    "理赔需要的材料清单与销售流程介绍",
    "本保险承保意外伤害导致的身故或残疾",
]


def tokenize(s: str) -> list:
    # 中文按"字"切(真实系统会用 jieba 等做词级切分)
    return list(re.sub(r"\s", "", s))


corpus = [tokenize(d) for d in docs]
N = len(corpus)
avgdl = sum(len(d) for d in corpus) / N

df = {}
for d in corpus:
    for term in set(d):
        df[term] = df.get(term, 0) + 1


def idf(term: str) -> float:
    # 稀有词 IDF 高(越少见越值钱)
    n = df.get(term, 0)
    return math.log(1 + (N - n + 0.5) / (n + 0.5))


def bm25(query: str, doc: list, k1: float = 1.5, b: float = 0.75) -> float:
    score, dl = 0.0, len(doc)
    for term in tokenize(query):
        if term not in doc:
            continue
        f = doc.count(term)                                  # 词频 TF
        tf_sat = f * (k1 + 1) / (f + k1 * (1 - b + b * dl / avgdl))  # 词频饱和 + 长度归一
        score += idf(term) * tf_sat                          # 乘以 IDF
    return score


if __name__ == "__main__":
    for q in ["等待期多久", "推销保险"]:
        print(f"query = {q}")
        ranked = sorted(range(N), key=lambda i: bm25(q, corpus[i]), reverse=True)
        for i in ranked:
            print(f"  score={bm25(q, corpus[i]):.2f}  {docs[i]}")
        print()
    print("观察:'等待期多久'精确命中术语,得分高且拉得开;")
    print("但'推销保险'里的'推销',BM25 没法匹配到文档里的'销售'——这就是它的硬伤。")
