"""
RAG 教程第 1 章 - 20 行迷你 RAG(零依赖)

不需要装任何库、不需要 API key,直接 python mini_rag_demo.py 就能跑。
目的:亲眼看到"检索到资料就照着答,没检索到就只能瞎猜(幻觉)"。

对应文章:https://www.wsxdmx.com/projects/rag-system/c/01-why-rag
"""

# 一个极简"知识库":真实场景里这会是几千份文档切成的 chunk + 向量
knowledge = {
    "犹豫期": "本产品犹豫期为 15 天,自您签收合同的次日 0 时起算。",
    "现金价值": "现金价值 = 累计已交保费 − 各项费用 − 风险保费,具体见合同附表。",
    "等待期": "本产品等待期为 90 天,等待期内出险不予赔付。",
}


def retrieve(question: str):
    """最朴素的'检索':哪个词出现在问题里,就召回哪条。真实系统会换成向量检索。"""
    for key, text in knowledge.items():
        if key in question:
            return text
    return None


def answer(question: str) -> str:
    ctx = retrieve(question)
    if ctx is None:
        return "【没检索到资料】模型只能凭记忆瞎猜——这就是幻觉的温床"
    return f"【检索到资料,照着答】依据:{ctx}"


if __name__ == "__main__":
    for q in ["犹豫期是多少天?", "现金价值怎么算?", "高原反应保不保?"]:
        print(q, "->", answer(q))
