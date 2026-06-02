"""一键建库脚本 —— 离线把 data/sample_docs/ 下的文档灌进向量库。

流程:加载 PDF → 结构感知切分 → bge-m3 向量化 → 写入 ChromaDB。
建一次库即可,之后反复用 scripts/ask.py 提问,不必每次重建。

依赖:sentence-transformers(首次会下载 bge-m3,约 2GB)+ chromadb。
不需要 DeepSeek key(建库只用本地 Embedding 模型)。

用法:python3 scripts/build_index.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rich.console import Console

from src.config import CHROMA_DIR, DATA_DIR

console = Console()


def main() -> None:
    if not any(DATA_DIR.glob("*.pdf")):
        console.print(
            "[red]❌ data/sample_docs/ 下没有 PDF。[/red]\n"
            "   先生成测试数据:python3 scripts/generate_synthetic_data.py"
        )
        sys.exit(1)

    console.print("🔧 装配 pipeline(首次会加载 bge-m3,可能要等一会儿)…")
    from src.pipeline import RAGPipeline  # 在校验之后再 import,避免无谓地拉起重型依赖

    pipe = RAGPipeline()
    console.print(f"📚 从 [bold]{DATA_DIR}[/bold] 建库…")
    n = pipe.build_index()
    total = pipe.store.count()
    console.print(f"\n✅ 建库完成:本次写入 [bold]{n}[/bold] 个 chunk,库中共 [bold]{total}[/bold] 个。")
    console.print(f"[dim]向量库位置:{CHROMA_DIR}[/dim]")
    console.print('\n下一步:python3 scripts/ask.py "等待期是多少天?"')


if __name__ == "__main__":
    main()
