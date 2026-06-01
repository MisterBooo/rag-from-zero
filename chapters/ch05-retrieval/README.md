# 第 5 章:检索召回 —— 混合检索(BM25 + 向量)

> 配套文章详解 → [网站文章](https://www.wsxdmx.com/projects/rag-system/c/05-retrieval)

## 你将学到

- 用纯 Python 实现关键词检索的标准算法 BM25
- 看清 BM25 的强项(精确命中术语)和硬伤(不懂近义词),理解为什么要做混合检索

## 运行

```bash
# 零依赖,直接跑
python bm25_demo.py
```

预期输出(节选):

```
query = 等待期多久
  score=4.51  等待期说明:本产品等待期为90天,等待期内出险不予赔付
  score=0.00  理赔需要的材料清单与销售流程介绍
  score=0.00  本保险承保意外伤害导致的身故或残疾
```

"等待期"被精确命中、得分一骑绝尘;而"推销保险"这种需要理解近义的查询,BM25 就抓瞎了——这正是要叠加向量检索的原因。

## 文件说明

- `bm25_demo.py` - 纯 Python 实现的 BM25(IDF + 词频饱和 + 文档长度归一)

## 配套文章

→ [www.wsxdmx.com/projects/rag-system/c/05-retrieval](https://www.wsxdmx.com/projects/rag-system/c/05-retrieval)
