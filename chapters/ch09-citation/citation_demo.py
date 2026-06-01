"""
RAG 教程第 9 章 - 零依赖"带引用 + 会拒答"的上下文问答 demo

不需要装任何库,直接 python citation_demo.py 就能跑。
目的:亲眼看到"上下文问答"的两条铁律——
  ① 答案每一句都标出处 [编号],可溯源;
  ② 资料里没有就老实拒答,而不是编一个(防幻觉)。

对应文章:https://www.wsxdmx.com/projects/rag-system/c/09-citation
"""

# 检索回来的候选片段(真实系统由第 5、6 章产出;每条带来源 src,对应第 3 章的 section_path)
CHUNKS = [
    {"id": 1, "src": "第2条 保险责任", "text": "本保险承保意外伤害导致的医疗费用,予以赔付。"},
    {"id": 2, "src": "第5条 等待期", "text": "等待期为 90 天,等待期内出险不予赔付。"},
    {"id": 3, "src": "第8条 责任免除", "text": "战争、核辐射导致的伤害不在保障范围内。"},
]


def retrieve(query: str, chunks: list, topk: int = 2, threshold: int = 3):
    """朴素检索:按"问题里的字命中 chunk 多少"打分(真实用第 5、6 章那套)。"""
    scored = []
    for c in chunks:
        hit = sum(1 for ch in set(query) if ch in c["text"])  # 命中字数
        scored.append((hit, c))
    scored.sort(key=lambda x: -x[0])                          # 分高的在前
    # 阈值=3:只共享一两个常用字(的/伤)不算命中,低于阈值视为"不相关",不硬塞给模型 —— 这是能"拒答"的前提
    return [c for hit, c in scored if hit >= threshold][:topk]


def answer_with_citation(query: str, chunks: list):
    """生成答案:有依据就照着答并标 [编号],没依据就拒答(绝不编)。"""
    hits = retrieve(query, chunks)
    if not hits:                                              # ① 没检索到相关片段
        return "【依据不足】资料里没有相关内容,无法回答。", []   #    → 拒答,而不是瞎编
    # ② 有依据:把每条片段当作答案,并在句末标上它的来源编号 [id]
    body = ";".join(f'{c["text"].rstrip("。")}[{c["id"]}]' for c in hits)
    refs = [(c["id"], c["src"]) for c in hits]                # 编号 → 来源,供前端映射回原文
    return "答:" + body + "。", refs


def show(query: str):
    ans, refs = answer_with_citation(query, CHUNKS)
    print(f"问:{query}")
    print(f"   {ans}")
    if refs:
        print("   引用:" + "  ".join(f"[{i}] {src}" for i, src in refs))
    print()


if __name__ == "__main__":
    print("=== 有依据:照着答 + 标出处 ===")
    show("意外受伤的医疗费用报销吗?")     # 命中第2条 → 带 [1] 作答

    print("=== 库里没有:老实拒答(不编) ===")
    show("癌症能赔吗?")                    # 没有相关片段 → 拒答,而不是编一个答案
