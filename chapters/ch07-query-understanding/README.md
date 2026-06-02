# 第 7 章:Query 理解与改写

> 配套文章详解 → [网站文章](https://www.wsxdmx.com/projects/rag-system/c/07-query-understanding)

## 你将学到

- 检索之前为什么要先"读懂、改好"用户问题
- 用零依赖代码看到 Query 重写(去口语)和扩写(加同义词)怎么救回检索

## 运行

> macOS / Linux 用 `python3` / `pip3`;Windows 用 `python` / `pip`(或 `py -3`)。跑不通看 [TROUBLESHOOTING.md](../../TROUBLESHOOTING.md)。

```bash
# 零依赖,直接跑
python3 query_rewrite_expand.py
```

预期输出:

```
① 原始 query: '请问保险理赔呢?' → 命中: []
② 重写后(去口语): '保险理赔' → 命中: ['保险理赔流程']
③ 扩写后(加同义词): ['保险理赔', '保险索赔'] → 命中: ['保险理赔流程', '保险索赔所需材料']
```

原始问题带口语词一条没命中;重写救回一条;扩写(理赔→索赔)又救回一条。

## 文件说明

- `query_rewrite_expand.py` - 零依赖的 Query 重写 + 扩写演示

## 配套文章

→ [www.wsxdmx.com/projects/rag-system/c/07-query-understanding](https://www.wsxdmx.com/projects/rag-system/c/07-query-understanding)
