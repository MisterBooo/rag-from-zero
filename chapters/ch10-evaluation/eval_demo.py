"""
RAG 教程第 10 章 - 零依赖检索评估脚本(Recall@k + MRR)

不需要装任何库,直接 python eval_demo.py 就能跑。
目的:把"感觉变好了"变成"数字说话"——用一个标好答案的小评估集,
      客观算出检索到底好不好(召回率 Recall@k、平均倒数排名 MRR)。

对应文章:https://www.wsxdmx.com/projects/rag-system/c/10-evaluation
"""

# 评估集:每道题事先人工标好"正确答案应该来自哪个 chunk"(ground-truth)
QA = [
    {"q": "犹豫期多久", "gold": "c1"},
    {"q": "等待期内出险赔吗", "gold": "c2"},
    {"q": "核辐射保不保", "gold": "c3"},
]

# 待评估的检索系统:对每个问题,返回按相关度排序的 chunk_id 列表
# (真实系统这里就是第 5、6 章的检索+重排产出;这里用固定结果便于演示)
RETRIEVED = {
    "犹豫期多久": ["c1", "c4", "c2"],        # gold=c1 排第 1 ✓
    "等待期内出险赔吗": ["c5", "c2", "c1"],   # gold=c2 排第 2 ✓
    "核辐射保不保": ["c4", "c5", "c6"],       # gold=c3 根本没召回 ✗
}


def recall_at_k(qa: list, retrieved: dict, k: int) -> float:
    """Recall@k:有多少题的正确 chunk,出现在了前 k 个检索结果里。"""
    hit = sum(1 for item in qa if item["gold"] in retrieved[item["q"]][:k])
    return hit / len(qa)


def mrr(qa: list, retrieved: dict) -> float:
    """MRR(平均倒数排名):正确 chunk 排得越靠前,分越高(排第1得1,第2得0.5…没召回得0)。"""
    total = 0.0
    for item in qa:
        ranked = retrieved[item["q"]]
        rank = ranked.index(item["gold"]) + 1 if item["gold"] in ranked else 0
        total += (1.0 / rank) if rank else 0.0   # 没召回到 → 这题贡献 0
    return total / len(qa)


if __name__ == "__main__":
    print("评估集共", len(QA), "道题\n")
    print(f"Recall@1 = {recall_at_k(QA, RETRIEVED, 1):.2f}   (只看排第1有没有命中)")
    print(f"Recall@3 = {recall_at_k(QA, RETRIEVED, 3):.2f}   (前3个里有没有命中)")
    print(f"MRR      = {mrr(QA, RETRIEVED):.2f}   (正确chunk的平均排名,越高越靠前)")
    print()
    print("解读:Recall@3=0.67 → 3 道题里 2 道在前3命中,1 道(核辐射)漏了;")
    print("     换个切分/检索方案再跑一次,这两个数字一对比,好坏一目了然。")
