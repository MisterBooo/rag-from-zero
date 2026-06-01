"""
RAG 教程第 2 章 - 端到端迷你 RAG 骨架(零依赖)

不需要装任何库、不需要 API key,直接 python mini_rag_pipeline.py 就能跑。
把"离线建库 + 在线问答"两条链路各写成几个函数——骨架和真实系统一样,
差别只在每一块的工程化深度(后面章节逐块替换)。

对应文章:https://www.wsxdmx.com/projects/rag-system/c/02-architecture
"""

# ============ 离线:建库(只跑一次 / 定期更新) ============

docs = [
    "第1条 责任范围:本保险承保意外伤害导致的身故或残疾,但以下情况除外:战争、核辐射。",
    "第2条 等待期:本产品等待期为90天,等待期内出险不予赔付。",
    "第3条 现金价值:现金价值等于累计已交保费扣除各项费用与风险保费。",
]


def chunk(text, size=20):
    """把一段长文本剪成多个小段(chunk)。

    Args:
        text: 一篇文档的全文
        size: 每段多少字(真实系统按"语义"切,见第 3 章;这里图省事按定长切)
    Returns:
        小段组成的列表
    """
    # 从 0 开始,每隔 size 个字截一段:text[0:20]、text[20:40] ……
    return [text[i:i + size] for i in range(0, len(text), size)]


def build_index(docs):
    """把所有文档切成 chunk,存成一个"能查的"列表 = 玩具版知识库。

    真实系统这一步会把每个 chunk 转成向量存进向量库 + 建倒排索引(第 4、5 章)。
    """
    index = []
    for doc_id, text in enumerate(docs):   # doc_id:记住这段来自第几篇文档(后面溯源用)
        for piece in chunk(text):          # 把这篇文档切成若干小段
            index.append({"doc_id": doc_id, "text": piece})
    return index


# ============ 在线:问答(每次提问都跑一遍) ============

def retrieve(index, query, top_k=2):
    """从知识库里找出最相关的 top_k 个 chunk。

    这里用最朴素的相似度:query 里有多少个字在 chunk 文本里出现过。
    真实系统换成向量相似度(第 4 章)+ BM25 关键词打分(第 5 章)。
    """
    scored = []
    for item in index:
        # 命中数:query 的每个字,只要在这个 chunk 文本里出现就 +1
        hit = sum(1 for ch in query if ch in item["text"])
        scored.append((hit, item))
    # 按命中数从高到低排序
    scored.sort(key=lambda x: x[0], reverse=True)
    # 取前 top_k 个,且至少命中 1 个字(命中 0 的直接丢掉)
    return [item for hit, item in scored[:top_k] if hit > 0]


def assemble_context(chunks):
    """把召回的 chunk 拼成一段"上下文",准备喂给大模型。

    每条都标上来源 doc_id;真实系统还会做 Prompt 模板 + 引用溯源(第 9 章)。
    """
    return "\n".join(f"[来源 doc{c['doc_id']}] {c['text']}" for c in chunks)


def answer(index, query):
    """完整走一遍:检索 → 拼上下文 →(交给模型)回答。"""
    hits = retrieve(index, query)          # ① 先检索:捞出相关的几段
    if not hits:                           # 一条都没召回 → 模型没依据,只能瞎猜
        return "没检索到 → 模型只能瞎猜(幻觉)"
    context = assemble_context(hits)       # ② 拼上下文
    # ③ 真实系统这里会把 context + query 拼成 prompt 发给 LLM;玩具版只打印模型会看到啥
    return f"模型将基于以下上下文作答:\n{context}"


if __name__ == "__main__":
    index = build_index(docs)              # 离线:建库(只跑一次)
    print(f"建库完成,共 {len(index)} 个 chunk\n")
    print(answer(index, "核辐射保不保"))    # 在线:每次提问跑一遍
