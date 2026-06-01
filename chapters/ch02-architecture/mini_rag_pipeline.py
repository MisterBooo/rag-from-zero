"""
RAG 教程第 2 章 - 端到端迷你 RAG 骨架(零依赖)

不需要装任何库、不需要 API key,直接 python mini_rag_pipeline.py 就能跑。
把"离线建库 + 在线问答"两条链路各写成几个函数——骨架和真实系统一样,
差别只在每一块的工程化深度(后面章节逐块替换)。

对应文章:https://www.wsxdmx.com/projects/rag-system/c/02-architecture
"""

# ============ 离线:建库 ============
docs = [
    "第1条 责任范围:本保险承保意外伤害导致的身故或残疾,但以下情况除外:战争、核辐射。",
    "第2条 等待期:本产品等待期为90天,等待期内出险不予赔付。",
    "第3条 现金价值:现金价值等于累计已交保费扣除各项费用与风险保费。",
]


def chunk(text, size=20):
    # 朴素切分:每 size 个字一段(真实用结构感知切分,见第 3 章)
    return [text[i:i + size] for i in range(0, len(text), size)]


def build_index(docs):
    # 朴素索引:一个 chunk 列表(真实用向量库 + 倒排索引,见第 4、5 章)
    index = []
    for doc_id, d in enumerate(docs):
        for c in chunk(d):
            index.append({"doc_id": doc_id, "text": c})
    return index


# ============ 在线:问答 ============
def retrieve(index, query, top_k=2):
    # 朴素检索:按"query 字符与 chunk 重合数"打分(真实用向量相似度 + BM25,见第 5、6 章)
    scored = [(sum(ch in c["text"] for ch in query), c) for c in index]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for s, c in scored[:top_k] if s > 0]


def assemble_context(chunks):
    # 把召回的块拼成上下文(真实还要做 Prompt 构建 + 引用溯源,见第 9 章)
    return "\n".join(f"[来源 doc{c['doc_id']}] {c['text']}" for c in chunks)


def answer(index, query):
    hits = retrieve(index, query)
    if not hits:
        return "没检索到 → 模型只能瞎猜(幻觉)"
    ctx = assemble_context(hits)
    # 真实这里会把 ctx + query 拼成 prompt 交给 LLM;这里只打印模型会看到什么
    return f"模型将基于以下上下文作答:\n{ctx}"


if __name__ == "__main__":
    index = build_index(docs)
    print(f"建库完成,共 {len(index)} 个 chunk\n")
    print(answer(index, "核辐射保不保"))
