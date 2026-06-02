"""
RAG 教程第 6 章 - 粗排会犯的错(零依赖)

不需要装任何库,直接 python3 rerank_demo.py 就能跑。
目的:用一个玩具「粗排」(只数字面重合、独立打分)亲眼看到它把"字面像但语义相反"的
免责条款排到了第一,从而理解为什么需要「精排」来纠正。

对应文章:https://www.wsxdmx.com/projects/rag-system/c/06-reranking
"""

query = "孩子摔伤住院,意外险能赔吗?"

candidates = [
    "第2条 保险责任:本保险承保意外伤害导致的医疗费用,予以赔付",  # ← 真正该答的
    "第3条 责任免除:孩子在学校受伤住院,属下列情形之一的不予赔付",  # ← 字面更像,却是反面
]


def coarse_score(q: str, doc: str) -> int:
    """玩具粗排:独立地数 query 的字在 doc 里命中多少(不理解 query 和 doc 的关系)。"""
    return sum(ch in doc for ch in set(q))


if __name__ == "__main__":
    ranked = sorted(candidates, key=lambda d: coarse_score(query, d), reverse=True)
    print(f"query = {query}\n粗排(按字面重合打分):")
    for i, d in enumerate(ranked):
        print(f"  #{i + 1}  score={coarse_score(query, d)}  {d}")

    print("\n看到了吗:字面命中更多的「责任免除」被排到了第一,")
    print("但它恰恰是反面——真正该答的「保险责任」反而被压下去了。")
    print("粗排独立打分,读不懂'免责'和问题意图是相反的 → 这正是精排要解决的。")
