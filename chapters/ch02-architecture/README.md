# 第 2 章:RAG 整体架构

> 配套文章详解 → [网站文章](https://www.wsxdmx.com/projects/rag-system/c/02-architecture)

## 你将学到

- RAG 的两条链路(离线建库 + 在线问答)
- 把架构图变成一段端到端、可运行的迷你 RAG 骨架

## 运行

```bash
# 不需要装任何库、不需要 API key
python mini_rag_pipeline.py
```

预期输出:

```
建库完成,共 7 个 chunk

模型将基于以下上下文作答:
[来源 doc0] 第1条 责任范围:本保险承保意外伤害导致
[来源 doc0] 的身故或残疾,但以下情况除外:战争、核辐
```

5 个函数(`chunk` / `build_index` / `retrieve` / `assemble_context` / `answer`)分别对应真实系统的解析切分、建索引、检索、拼上下文、生成——骨架一样,后面章节逐块换成生产版。

## 配套文章

→ [www.wsxdmx.com/projects/rag-system/c/02-architecture](https://www.wsxdmx.com/projects/rag-system/c/02-architecture)
