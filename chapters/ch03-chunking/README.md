# 第 3 章:文档预处理与切分

> 配套文章详解 → [网站文章](https://www.wushixiongai.com/projects/rag-system/c/03-chunking)

## 你将学到

- chunk_size / chunk_overlap 参数的影响
- 用 RecursiveCharacterTextSplitter 切分一份 PDF
- 复现真实生产中"切分错位"导致的事故

## 运行

> macOS / Linux 用 `python3` / `pip3`;Windows 用 `python` / `pip`(或 `py -3`)。跑不通看 [TROUBLESHOOTING.md](../../TROUBLESHOOTING.md)。

```bash
pip3 install -r requirements.txt

# 准备一份 PDF 命名为 your_doc.pdf,然后:
python3 chunk_demo.py

# 复现核辐射事故:
python3 reproduce-disaster.py
```

## 文件说明

- `chunk_demo.py` - 主示例,展示基础切分
- `reproduce-disaster.py` - 重现固定长度切分导致的事故
- `requirements.txt` - 依赖
- `sample-data/` - 测试样本说明

## 配套文章

完整讲解(含原理 + 三代演进 + 真实事故 + 5 个工程招式)在网站:

→ [www.wushixiongai.com/projects/rag-system/c/03-chunking](https://www.wushixiongai.com/projects/rag-system/c/03-chunking)
