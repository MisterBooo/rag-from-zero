<div align="center">
  <h1>🎬 RAG From Zero</h1>
  <p><strong>从零做出能上线的 RAG 系统,跟着代码学,完整开源</strong></p>

  <p>
    <img src="https://img.shields.io/github/stars/MisterBooo/rag-from-zero?style=social">
    <img src="https://img.shields.io/github/forks/MisterBooo/rag-from-zero?style=social">
    <img src="https://img.shields.io/badge/教程章节-10+1-blue">
    <img src="https://img.shields.io/badge/license-MIT-green">
  </p>

  <p>
    🌐 <a href="https://www.wsxdmx.com/projects/rag-system">在网站看完整教程</a>
    ·
    💻 <a href="#章节代码">直接看代码</a>
    ·
    ⭐ Star 一下支持
  </p>
</div>

---

## 这个项目是什么

我是 [@MisterBooo](https://github.com/MisterBooo),5 年前我做了 [LeetCodeAnimation](https://github.com/MisterBooo/LeetCodeAnimation)(76.7k stars,用动画讲算法)。

2026 年,我把同样的"图解 + 实战"方法用在大模型上,做了这个 RAG 教程项目。

**特点**:
- 📖 完整 10 章教程,从概念到上线
- 💻 每章配套完整可运行代码,clone 下来就能跑
- 📊 每章 5+ 张原创图,把抽象概念可视化
- 🎯 每章配套大厂面试题,学完直接面试用

完整文章在 → [www.wsxdmx.com/projects/rag-system](https://www.wsxdmx.com/projects/rag-system)

## 章节代码

| 章节 | 主题 | 代码 | 文章 |
|------|------|------|------|
| 第 1 章 | 为什么做 RAG | [→ 代码](chapters/ch01-why-rag/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/01-why-rag) |
| 第 2 章 | RAG 整体架构 | [→ 代码](chapters/ch02-architecture/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/02-architecture) |
| 第 3 章 | 文档预处理与切分 | [→ 代码](chapters/ch03-chunking/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/03-chunking) |
| 第 4 章 | Embedding 选型 | [→ 代码](chapters/ch04-embedding/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/04-embedding) |
| 第 5 章 | 检索召回 | [→ 代码](chapters/ch05-retrieval/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/05-retrieval) |
| 第 6 章 | 重排与检索优化 | [→ 代码](chapters/ch06-reranking/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/06-reranking) |
| 第 7 章 | Query 理解与改写 | [→ 代码](chapters/ch07-query-understanding/) | [→ 阅读](https://www.wsxdmx.com/projects/rag-system/c/07-query-understanding) |
| ... | ... | ... | ... |

## 快速开始

```bash
git clone https://github.com/MisterBooo/rag-from-zero.git
cd rag-from-zero/chapters/ch03-chunking
pip install -r requirements.txt
python chunk_demo.py
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
