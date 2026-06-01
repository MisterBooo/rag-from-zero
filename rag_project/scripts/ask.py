"""完整版问答 —— 调用 src/pipeline.py 的端到端链路。

链路:Query 改写(第7章)→ 向量+BM25 双路检索(第5章)→ Cross-Encoder 重排(第6章)
     → 带引用的答案生成(第9章)。

前置:
  1) python scripts/generate_synthetic_data.py   # 造测试 PDF
  2) python scripts/build_index.py                # 建向量库(只需一次)
  3) cp .env.example .env 并填入 DEEPSEEK_API_KEY  # 生成答案需要

用法:python scripts/ask.py "等待期是多少天?"

提示:想 30 秒先跑通、不建库不下模型,用 scripts/quickstart.py。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rich.console import Console

from src.config import validate_config

console = Console()


def main() -> None:
    if len(sys.argv) < 2:
        console.print('用法: [bold]python scripts/ask.py "你的问题"[/bold]')
        sys.exit(1)

    validate_config()  # 没配 DEEPSEEK_API_KEY 会给出清晰中文提示
    query = sys.argv[1]

    console.print("🔧 装配 pipeline(首次会加载本地模型,稍候)…")
    from src.pipeline import RAGPipeline

    pipe = RAGPipeline()
    if pipe.store.count() == 0:
        console.print(
            "[yellow]⚠️  向量库是空的,请先建库:python scripts/build_index.py[/yellow]\n"
            '   (或先用 python scripts/quickstart.py "你的问题" 免建库快速体验)'
        )
        sys.exit(1)

    console.print(f"💬 提问:[bold]{query}[/bold]\n")
    answer = pipe.ask(query)

    console.print(f"[bold green]答案:[/bold green]\n{answer.text}\n")
    if answer.sources:
        console.print(f"[dim]来源:{', '.join(answer.sources)}[/dim]")


if __name__ == "__main__":
    main()
