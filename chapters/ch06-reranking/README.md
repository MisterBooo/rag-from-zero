# 第 6 章:重排(Rerank)与检索优化

> 配套文章详解 → [网站文章](https://www.wushixiongai.com/projects/rag-system/c/06-reranking)

## 你将学到

- 为什么"粗排"会把字面像、语义相反的文档排错,精排怎么纠正
- 用真实开源 Cross-Encoder 给检索结果重排

## 运行

> macOS / Linux 用 `python3` / `pip3`;Windows 用 `python` / `pip`(或 `py -3`)。跑不通看 [TROUBLESHOOTING.md](../../TROUBLESHOOTING.md)。

```bash
# 玩具版:零依赖,看粗排怎么排错
python3 rerank_demo.py

# 真实版:装库后跑,看 Cross-Encoder 把正确条款排回第一
pip3 install sentence-transformers
python3 real_rerank.py
```

`rerank_demo.py` 预期输出:

```
  #1  score=7  第3条 责任免除:孩子在学校受伤住院,属下列情形之一的不予赔付
  #2  score=6  第2条 保险责任:本保险承保意外伤害导致的医疗费用,予以赔付
```

字面命中更多的「免责」被排到第一,真正该答的「保险责任」被压下去——这就是要精排的原因。

## 文件说明

- `rerank_demo.py` - 零依赖玩具粗排,演示"独立打分"会排错
- `real_rerank.py` - 用开源 Cross-Encoder 精排(需 sentence-transformers)

## 配套文章

→ [www.wushixiongai.com/projects/rag-system/c/06-reranking](https://www.wushixiongai.com/projects/rag-system/c/06-reranking)
