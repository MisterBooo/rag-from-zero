"""极简问答(30 秒建立信心)—— 不建向量库、不下载 Embedding 模型。

它故意用最朴素的 ad-hoc 逻辑(读 PDF → 定长切分 → 关键词检索 → 调 LLM),
只依赖 openai / pypdf / rich,跑得飞快,用来确认「环境通了、能跑出答案」。
想看完整的向量检索 + 重排 + 引用,请用 build_index.py + ask.py。

用法:python3 scripts/quickstart.py "等待期是多少天?"
"""

import sys
from pathlib import Path

# 让脚本无论从哪个目录运行,都能 import 到 src.config
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from openai import OpenAI
from pypdf import PdfReader
from rich.console import Console

from src.config import (
    DATA_DIR,
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    LLM_MODEL,
    LLM_TEMPERATURE,
    validate_config,
)

console = Console()


def load_all_pdfs() -> list[dict]:
    """加载 data/sample_docs/ 下所有 PDF,返回 [{source, text}, ...]。"""
    docs = []
    for pdf_path in sorted(DATA_DIR.glob("*.pdf")):
        text = "".join(page.extract_text() or "" for page in PdfReader(pdf_path).pages)
        docs.append({"source": pdf_path.name, "text": text})
    return docs


def naive_chunk(text: str, size: int = 120) -> list[str]:
    """最朴素的定长切分(完整结构感知切分见 src/chunker.py)。"""
    text = text.replace("\n", "")
    return [text[i : i + size] for i in range(0, len(text), size) if text[i : i + size].strip()]


def naive_retrieve(chunks: list[dict], query: str, top_k: int = 3) -> list[dict]:
    """关键词字符重合度检索(向量 + BM25 混合检索见 src/retriever.py)。"""
    scored = []
    for c in chunks:
        score = sum(1 for ch in set(query) if ch.strip() and ch in c["text"])
        if score > 0:
            scored.append((score, c))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [c for _, c in scored[:top_k]]


def ask_llm(query: str, contexts: list[dict]) -> str:
    """把上下文塞进 prompt,调 DeepSeek 生成答案。"""
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
    context_text = "\n\n".join(f"[来源:{c['source']}]\n{c['text']}" for c in contexts)
    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        messages=[
            {
                "role": "system",
                "content": "你是严谨的保险客服。只能依据提供的上下文回答;"
                "上下文里没有的信息,请直接说「根据现有资料无法确定」,不要编造。",
            },
            {"role": "user", "content": f"上下文:\n{context_text}\n\n问题:{query}"},
        ],
    )
    return response.choices[0].message.content or ""


def main() -> None:
    if len(sys.argv) < 2:
        console.print('用法: [bold]python3 scripts/quickstart.py "你的问题"[/bold]')
        sys.exit(1)

    validate_config()
    query = sys.argv[1]

    console.print("📚 加载文档…")
    docs = load_all_pdfs()
    if not docs:
        console.print("[red]❌ data/sample_docs/ 下没有 PDF,请先运行:python3 scripts/generate_synthetic_data.py[/red]")
        sys.exit(1)

    console.print("✂️  切分…")
    chunks = [{"source": d["source"], "text": ct} for d in docs for ct in naive_chunk(d["text"])]

    console.print("🔍 检索…")
    contexts = naive_retrieve(chunks, query)
    if not contexts:
        console.print("[yellow]⚠️  没检索到相关内容,换个更具体的问法试试。[/yellow]")
        sys.exit(0)
    console.print(f"📎 检索到 [bold]{len(contexts)}[/bold] 段相关上下文\n")

    console.print("💬 生成答案中…\n")
    answer = ask_llm(query, contexts)

    console.print(f"[bold green]答案:[/bold green]\n{answer}\n")
    sources = sorted({c["source"] for c in contexts})
    console.print(f"[dim]来源:{', '.join(sources)}[/dim]")


if __name__ == "__main__":
    main()
