<div align="center">
  <h1>🎬 RAG From Zero</h1>
  <p><strong>从零做出能上线的 RAG 系统,跟着代码学,完整开源</strong></p>

  <p>
    <img src="https://img.shields.io/github/stars/MisterBooo/rag-from-zero?style=social">
    <img src="https://img.shields.io/github/forks/MisterBooo/rag-from-zero?style=social">
    <img src="https://img.shields.io/badge/教程章节-10%20章%20%2B%20附录-blue">
    <img src="https://img.shields.io/badge/license-MIT-green">
  </p>

  <p>
    🌐 <a href="https://www.wsxdmx.com/projects/rag-system">在网站看完整教程</a>
    ·
    🛠️ <a href="#可运行的端到端项目">跑起来一个完整 RAG</a>
    ·
    💻 <a href="#章节代码">看章节代码</a>
    ·
    ⭐ Star 一下支持
  </p>
</div>

---

## 这个项目是什么

我是 [@MisterBooo](https://github.com/MisterBooo),5 年前我做了 [LeetCodeAnimation](https://github.com/MisterBooo/LeetCodeAnimation)(76.7k stars,用动画讲算法)。

2026 年,我把同样的「图解 + 实战」方法用在大模型上,做了这个 RAG 教程项目。

**特点**:
- 📖 完整 **10 章 + 附录**,从「为什么做 RAG」一路讲到「上线优化」和「写进简历」
- 💻 每章配套**零依赖可运行 demo**(几十行,clone 下来就能跑),外加一个**完整的端到端项目**
- 📊 每章 **8–9 张原创图解**,把抽象概念可视化
- 🎯 每章配套大厂面试题 + 自检清单,学完直接面试用

完整文章在 → [www.wsxdmx.com/projects/rag-system](https://www.wsxdmx.com/projects/rag-system)

## 可运行的端到端项目

[`rag_project/`](rag_project/) 是一个**真正能跑**的 RAG 系统:DeepSeek + ChromaDB + bge-m3,
核心代码全手写、**没有 LangChain**,每个模块对应教程一章。

```bash
git clone https://github.com/MisterBooo/rag-from-zero.git
cd rag-from-zero/rag_project

# 先跑零依赖冒烟测试,确认逻辑没问题(不需要 key、不下模型)
python tests/smoke_test.py

# 完整链路:造数据 → 建向量库 → 提问(需 DeepSeek key + 本地模型)
pip install -r requirements.txt
cp .env.example .env            # 填入 DEEPSEEK_API_KEY
python scripts/generate_synthetic_data.py
python scripts/build_index.py
python scripts/ask.py "核辐射保不保?"
```

详细说明(含「30 秒免建库快速体验」路径)见 **[rag_project/README.md](rag_project/README.md)**。

## 章节代码

每章 `chapters/chNN-*/` 下都是**零依赖、可直接 `python xxx.py`** 的 demo(除第 3 章用到 langchain)。

| 章节 | 主题 | 代码 | 文章 |
|------|------|------|------|
| 第 1 章 | 为什么做 RAG | [→ 代码](chapters/ch01-why-rag/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/01-why-rag) |
| 第 2 章 | RAG 整体架构 | [→ 代码](chapters/ch02-architecture/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/02-architecture) |
| 第 3 章 | 文档预处理与切分 | [→ 代码](chapters/ch03-chunking/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/03-chunking) |
| 第 4 章 | Embedding 选型与向量化 | [→ 代码](chapters/ch04-embedding/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/04-embedding) |
| 第 5 章 | 检索召回 · 混合检索 | [→ 代码](chapters/ch05-retrieval/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/05-retrieval) |
| 第 6 章 | 重排与检索优化 | [→ 代码](chapters/ch06-reranking/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/06-reranking) |
| 第 7 章 | Query 理解与改写 | [→ 代码](chapters/ch07-query-understanding/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/07-query-understanding) |
| 第 8 章 | 多轮对话与记忆管理 | [→ 代码](chapters/ch08-memory/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/08-memory) |
| 第 9 章 | 上下文问答与引用溯源 | [→ 代码](chapters/ch09-citation/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/09-citation) |
| 第 10 章 | 系统评估与上线优化 | [→ 代码](chapters/ch10-evaluation/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/10-evaluation) |
| 附录 | 写进简历 & 面试应答 | [→ 模板](chapters/appendix-resume-interview/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/appendix-resume-interview) |

## 仓库结构

```
rag-from-zero/
├── README.md                  ← 你正在看的文件
├── LICENSE                    ← MIT
├── chapters/                  ← 每章一个目录:可运行 demo + 章节说明
│   ├── ch01-why-rag/ … ch10-evaluation/
│   └── appendix-resume-interview/   ← 简历填空模板
└── rag_project/               ← 完整端到端项目(DeepSeek + ChromaDB,手写无 LangChain)
    ├── src/                   ← 9 个核心模块,各对应一章
    ├── scripts/               ← 造数据 / 建库 / 问答
    └── tests/                 ← 零依赖冒烟测试 + 评估集
```

## 快速开始(章节 demo)

```bash
git clone https://github.com/MisterBooo/rag-from-zero.git
cd rag-from-zero/chapters/ch05-retrieval
python bm25_demo.py          # 纯 Python 手写 BM25,零依赖,直接跑
```

## 关于作者

- 📚 [LeetCodeAnimation](https://github.com/MisterBooo/LeetCodeAnimation) - 76.7k stars
- 🌐 [wsxdmx.com](https://www.wsxdmx.com) - 大模型面试题库
- 📱 微信公众号:**吴师兄学大模型**

## License

MIT - 自由使用,商用请保留署名

---

⭐ 如果对你有帮助,**给个 Star** 就是对我最大的支持。

<sub>ℹ️ 本仓库由主仓库自动同步生成(源目录 `docs/v2-rag-project/github-repo/`,push 到 `production` 分支时通过 `rsync --delete` 同步)。**因此请勿直接在本仓库修改**——直接改动会被下次同步覆盖。Issue 欢迎在此提;代码贡献请在源仓库发起。</sub>
