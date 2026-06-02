"""
RAG 教程第 3 章 - 基础切分演示

用法:
    1. 准备一份 PDF 文件,命名为 your_doc.pdf 放到当前目录
    2. python3 chunk_demo.py   # macOS / Linux;Windows: python chunk_demo.py

对应文章:https://www.wsxdmx.com/projects/rag-system/c/03-chunking
"""

import sys
from pathlib import Path

try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ImportError as e:
    print(f"❌ 缺少依赖({e.name}),装好再跑:")
    print("")
    print("  macOS / Linux:  pip3 install -r requirements.txt")
    print("  Windows:        pip install -r requirements.txt")
    print("")
    print("  pypi 慢就加清华镜像:")
    print("    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple")
    print("")
    print("  报 SSL: CERTIFICATE_VERIFY_FAILED(python.org 官方包):")
    print("    /Applications/Python\\ 3.13/Install\\ Certificates.command  # 3.13 换成你的版本")
    sys.exit(1)


def chunk_pdf(pdf_path: str, chunk_size: int = 512, chunk_overlap: int = 50):
    """切分一份 PDF 文档

    Args:
        pdf_path: PDF 文件路径
        chunk_size: 每个 chunk 的目标长度(字符数)
        chunk_overlap: 相邻 chunk 的重叠字符数

    Returns:
        (原文本, 切分后的 chunk 列表)
    """
    # 1. 读 PDF
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    text = "\n".join(d.page_content for d in docs)

    # 2. 切分
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。", "!", "?", ";", " ", ""],
    )
    return text, splitter.split_text(text)


def main():
    pdf_path = "your_doc.pdf"

    if not Path(pdf_path).exists():
        print(f"找不到 {pdf_path},请在当前目录放一份 PDF")
        return

    text, chunks = chunk_pdf(pdf_path)

    print(f"原文档总长度:{len(text)} 字")
    print(f"切完共 {len(chunks)} 个 chunk\n")
    print("第一个 chunk:")
    print(chunks[0])
    print("\n第二个 chunk(开头约 50 字和上一块重叠):")
    print(chunks[1])


if __name__ == "__main__":
    main()
