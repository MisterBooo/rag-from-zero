"""
重现教学失败场景:固定长度切分导致"核辐射"条款语义割裂

对应文章:https://www.wsxdmx.com/projects/rag-system/c/03-chunking
"""

import sys

try:
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


def main():
    text = "本保险承保意外伤害导致的身故或残疾,但以下情况除外:(1)战争 (2)核辐射"

    # 极小的 chunk_size,并让它在冒号/句号处断开,演示"从中间切断"的风险
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=30,
        chunk_overlap=0,
        separators=[":", "。", ""],
    )
    chunks = splitter.split_text(text)

    print("=== 固定长度切分的失败演练 ===\n")
    for i, c in enumerate(chunks):
        print(f"Chunk {i}: {c}\n")

    print("=== 用户问:核辐射在保障范围内吗? ===")
    print("→ Chunk 0 只到'但以下情况除外'就断了,除外项全在 Chunk 1")
    print("→ 检索只命中 Chunk 0,模型看不到核辐射属于除外项")
    print("→ 模型可能回答'在保障范围内' → 教学场景:残缺证据沿生成链路放大")


if __name__ == "__main__":
    main()
