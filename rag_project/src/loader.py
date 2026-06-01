"""PDF 加载模块 —— 对应文章第 3 章(文档预处理与切分)的「加载」环节。

把磁盘上的 PDF 读成纯文本 + 元数据,交给下游切分。
对应文章:https://www.wsxdmx.com/projects/rag-system/c/03-chunking
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LoadedDoc:
    """加载后的单篇文档。"""

    source: str  # 文件名,用于溯源(答案里告诉用户出处)
    text: str  # 抽取出的全文纯文本
    metadata: dict = field(default_factory=dict)  # 页数、字数等附加信息


def load_pdf(path: Path) -> LoadedDoc:
    """加载单个 PDF 文件为 LoadedDoc。

    Args:
        path: PDF 文件路径

    Returns:
        LoadedDoc:含全文文本与来源元数据
    """
    from pypdf import PdfReader  # 惰性导入:只有真用到 PDF 时才依赖 pypdf

    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(pages)
    return LoadedDoc(
        source=path.name,
        text=text,
        metadata={"num_pages": len(pages), "num_chars": len(text)},
    )


def load_dir(dir_path: Path) -> list[LoadedDoc]:
    """加载目录下所有 PDF。

    Args:
        dir_path: 存放 PDF 的目录(默认 data/sample_docs/)

    Returns:
        LoadedDoc 列表,每个 PDF 一个(按文件名排序,保证可复现)
    """
    docs: list[LoadedDoc] = []
    for pdf_path in sorted(Path(dir_path).glob("*.pdf")):
        doc = load_pdf(pdf_path)
        if doc.text.strip():  # 跳过没抽出文本的空 PDF
            docs.append(doc)
    return docs
