"""
RAG 教程第 7 章 - Query 重写 + 扩写(零依赖)

不需要装任何库,直接 python query_rewrite_expand.py 就能跑。
目的:亲眼看到「重写」(去口语)和「扩写」(加同义词)各自怎么把原本检索不到的问题救回来。

对应文章:https://www.wsxdmx.com/projects/rag-system/c/07-query-understanding
"""

docs = ["保险理赔流程", "保险索赔所需材料", "保险产品销售技巧"]

SYNONYMS = {"理赔": ["理赔", "索赔"]}  # 真实系统会用领域词典 / 词向量 / LLM 生成
FILLER = ["请问", "怎么", "一下", "呢", "啊", "?", "？"]  # 真实还会纠错、术语标准化(中英文问号都列上)


def rewrite(q: str) -> str:
    """重写:去掉口语词,得到更规范、更贴近书面表达的 query。"""
    for f in FILLER:
        q = q.replace(f, "")
    return q.strip()


def expand(q: str) -> list[str]:
    """扩写:对命中的词替换同义词,生成多个查询一起检索。"""
    out = {q}
    for word, syns in SYNONYMS.items():
        if word in q:
            out.update(q.replace(word, s) for s in syns)
    return sorted(out)


def search(queries: list[str]) -> list[str]:
    """朴素检索:doc 是否包含某个 query(真实系统换成向量/BM25)。"""
    return [d for d in docs if any(q in d for q in queries)]


if __name__ == "__main__":
    raw = "请问保险理赔呢?"
    print("① 原始 query:", repr(raw), "→ 命中:", search([raw]))
    r = rewrite(raw)
    print("② 重写后(去口语):", repr(r), "→ 命中:", search([r]))
    e = expand(r)
    print("③ 扩写后(加同义词):", e, "→ 命中:", search(e))

    print("\n原始问题因为带口语词,一条都没命中;")
    print("重写救回了「理赔流程」;扩写(理赔→索赔)又救回了用'索赔'表述的「索赔材料」。")
