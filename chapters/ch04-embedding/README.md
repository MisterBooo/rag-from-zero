# 第 4 章:Embedding 选型与向量化

> 配套文章详解 → [网站文章](https://www.wsxdmx.com/projects/rag-system/c/04-embedding)

## 你将学到

- "文字 → 向量 → 算距离"的核心机制,以及"数词重合"为什么不如学习得到的 Embedding
- 用真实开源模型(BGE)做一次语义检索

## 运行

> macOS / Linux 用 `python3` / `pip3`;Windows 用 `python` / `pip`(或 `py -3`)。跑不通看 [TROUBLESHOOTING.md](../../TROUBLESHOOTING.md)。

```bash
# 玩具版:零依赖,直接跑,看清"不懂近义词"的硬伤
python3 toy_embedding.py

# 真实版:装库后跑,看"索赔方法"也能匹配上"理赔"
pip3 install sentence-transformers
python3 real_embedding.py
```

`toy_embedding.py` 预期输出:

```
query = 保险理赔

  cos=0.50  理赔流程说明
  cos=0.25  索赔方法介绍
  cos=0.00  等待期是多久
```

"索赔方法"明明和"理赔"是一个意思却只拿 0.25 —— 这就是为什么要用学习得到的 Embedding。

## 文件说明

- `toy_embedding.py` - 零依赖玩具向量化,演示机制和硬伤
- `real_embedding.py` - 用开源 BGE 做语义检索(需 sentence-transformers)

## 配套文章

→ [www.wsxdmx.com/projects/rag-system/c/04-embedding](https://www.wsxdmx.com/projects/rag-system/c/04-embedding)
