# RAG From Zero · 端到端项目

> 一个**真正能跑**的 RAG 系统:DeepSeek + ChromaDB + bge-m3,核心代码全手写,**没有 LangChain**。
> 每个模块对应教程一章,读文章 + 看代码效果最好 → [www.wsxdmx.com/projects/rag-system](https://www.wsxdmx.com/projects/rag-system)

---

## 两条上手路径

| 路径 | 需要什么 | 用来干嘛 |
|------|---------|---------|
| 🅰️ **快速体验**(30 秒) | 只要 DeepSeek key | 不建库、不下模型,关键词检索 + LLM,先确认「能跑出答案」 |
| 🅱️ **完整链路**(推荐) | key + 本地模型(约 2GB) | 向量+BM25 检索 → 重排 → 带引用生成,就是文章讲的那套 |

### 路径 A:快速体验

```bash
cd rag_project
pip install openai pypdf reportlab rich          # 轻量依赖即可
cp .env.example .env                              # 填入 DEEPSEEK_API_KEY
python scripts/generate_synthetic_data.py         # 造 3 份虚构保险 PDF
python scripts/quickstart.py "等待期是多少天?"     # 朴素检索 + LLM,秒出答案
```

### 路径 B:完整链路

```bash
cd rag_project
pip install -r requirements.txt                   # 含 chromadb + sentence-transformers
cp .env.example .env                              # 填入 DEEPSEEK_API_KEY
python scripts/generate_synthetic_data.py         # 造测试 PDF
python scripts/build_index.py                      # 切分 + bge-m3 向量化 + 入 ChromaDB(只需一次)
python scripts/ask.py "核辐射保不保?"             # 改写→双路检索→重排→带引用生成
```

预期输出(大意):

```
💬 提问:核辐射保不保?

答案:
根据条款,核爆炸、核辐射或核污染属于「责任免除」范围,不予赔付 [1]。
来源:insurance_policy_v1.pdf
```

> 申请 DeepSeek key:https://platform.deepseek.com/api_keys

---

## 先跑一下冒烟测试(不需要 key、不下模型)

想在装一堆依赖之前,先确认核心逻辑没问题?跑这个零依赖测试:

```bash
python tests/smoke_test.py
```

它用「假 Embedder + 内存向量库」替换重型组件,但**真实地**跑切分、向量+BM25+RRF 融合、
Query 改写、带引用 prompt 构造、拒答——几秒钟验证整条装配链路逻辑正确。

---

## 项目结构

```
rag_project/
├── README.md                  ← 你正在看的文件
├── requirements.txt           ← 依赖(已钉版本)
├── .env.example               ← 配置模板,复制成 .env 填 key
│
├── src/                       ← 核心模块,每个对应教程一章,全部已实现
│   ├── config.py              ← 集中配置(路径 / key / 各种默认参数)
│   ├── loader.py              ← PDF 加载(第 3 章)
│   ├── chunker.py             ← 结构感知切分(第 3 章)
│   ├── embedder.py            ← bge-m3 向量化(第 4 章,惰性加载)
│   ├── vectorstore.py         ← ChromaDB 封装(第 5 章)
│   ├── retriever.py           ← 向量 + BM25 双路 + RRF 融合(第 5 章)
│   ├── reranker.py            ← Cross-Encoder 重排(第 6 章,惰性加载)
│   ├── query_processor.py     ← Query 改写 / 扩展(第 7 章,无 key 自动降级规则版)
│   ├── generator.py           ← 调 LLM 生成带引用的答案 + 拒答(第 9 章)
│   └── pipeline.py            ← 把以上串成完整链路(build_index / ask)
│
├── scripts/
│   ├── generate_synthetic_data.py  ← 合成测试 PDF
│   ├── quickstart.py               ← 路径 A:免建库快速体验
│   ├── build_index.py              ← 路径 B:建向量库
│   └── ask.py                      ← 路径 B:完整链路问答
│
├── tests/
│   ├── smoke_test.py          ← 零依赖冒烟测试(核查装配逻辑)
│   └── sample_qa.jsonl        ← 评估集:20 道问答 + 标准答案(配合第 10 章评估)
│
├── data/sample_docs/          ← 合成 PDF(运行脚本后生成,.gitignore)
└── chroma_data/               ← 向量库(build_index 后生成,.gitignore,可随时重建)
```

> 重型依赖(chromadb / sentence-transformers / openai)都是**惰性导入**——只 import
> `src` 不会触发模型下载或要求 key,所以冒烟测试和 CI 能零依赖跑起来。

## 对应文章

`src/` 每个模块都对应教程中的一章:

| 模块 | 对应文章 |
|------|---------|
| `loader.py` / `chunker.py` | [第 3 章 · 文档预处理与切分](https://www.wsxdmx.com/projects/rag-system/c/03-chunking) |
| `embedder.py` | [第 4 章 · Embedding 选型](https://www.wsxdmx.com/projects/rag-system/c/04-embedding) |
| `vectorstore.py` / `retriever.py` | [第 5 章 · 检索召回](https://www.wsxdmx.com/projects/rag-system/c/05-retrieval) |
| `reranker.py` | [第 6 章 · 重排与检索优化](https://www.wsxdmx.com/projects/rag-system/c/06-reranking) |
| `query_processor.py` | [第 7 章 · Query 理解与改写](https://www.wsxdmx.com/projects/rag-system/c/07-query-understanding) |
| `generator.py` | [第 9 章 · 上下文问答与引用溯源](https://www.wsxdmx.com/projects/rag-system/c/09-citation) |
| `tests/sample_qa.jsonl` | [第 10 章 · 系统评估与上线优化](https://www.wsxdmx.com/projects/rag-system/c/10-evaluation) |

## 测试数据说明

`scripts/generate_synthetic_data.py` 生成 3 份**完全虚构**的保险 PDF:

- `insurance_policy_v1.pdf` —— 主条款(等待期 90 天、犹豫期 15 天、现金价值公式、核辐射除外等)
- `claim_guide.pdf` —— 理赔指南(报案、资料、时效、拒赔原因)
- `product_brochure.pdf` —— 产品手册(营销口吻,与条款互为「同一事实不同表述」)

内容刻意与教程文章的案例呼应,方便你用代码亲手复现文章里讲到的现象。

## 常见问题

- **`❌ 缺少 DEEPSEEK_API_KEY`**:`cp .env.example .env` 后编辑 `.env` 填入即可。
- **`pip install` 慢 / 卡在 torch、chromadb**:`sentence-transformers` 会带 PyTorch,体积大;
  建议国内镜像:`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`。
  只想跑路径 A 的话,装 `openai pypdf reportlab rich` 就够了。
- **`ask.py` 提示向量库是空的**:先 `python scripts/build_index.py` 建库;或用 `quickstart.py` 免建库。
- **没装 sentence-transformers / chromadb,只想验证逻辑**:跑 `python tests/smoke_test.py`(零依赖)。
- **想关掉重排 / 改写先跑通**:在 `.env` 里设 `USE_RERANK=0`、`USE_QUERY_REWRITE=0`。
- **PDF 里中文乱码**:本项目用 reportlab 内置 `STSong-Light` 字体生成,跨平台正常。

## License

MIT
