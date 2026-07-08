# 第 1 章:为什么做 RAG

> 配套文章详解 → [网站文章](https://www.wushixiongai.com/projects/rag-system/c/01-why-rag)

## 你将学到

- RAG 最核心的一条流水线:检索 → 拼上下文 → 照着答
- 用一个**零依赖**的迷你 RAG,亲眼看到"检索到就照着答,没检索到就瞎猜(幻觉)"

## 运行

> macOS / Linux 用 `python3` / `pip3`;Windows 用 `python` / `pip`(或 `py -3`)。跑不通看 [TROUBLESHOOTING.md](../../TROUBLESHOOTING.md)。

```bash
# 不需要装任何库、不需要 API key
python3 mini_rag_demo.py
```

预期输出:

```
犹豫期是多少天? -> 【检索到资料,照着答】依据:本产品犹豫期为 15 天……
现金价值怎么算? -> 【检索到资料,照着答】依据:现金价值 = 累计已交保费……
高原反应保不保? -> 【没检索到资料】模型只能凭记忆瞎猜——这就是幻觉的温床
```

第三行没命中知识库,正是"私域盲区":库里没有,模型就只能编。

## 配套文章

→ [www.wushixiongai.com/projects/rag-system/c/01-why-rag](https://www.wushixiongai.com/projects/rag-system/c/01-why-rag)
