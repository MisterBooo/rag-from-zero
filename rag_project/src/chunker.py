"""文档切分模块 —— 对应文章第 3 章(文档预处理与切分)。

把长文本切成带元数据的小块(chunk)。切分质量直接决定检索质量——
文章开篇的「核辐射条款被从中间切断」事故,就是切分没做好导致的。

这里做的是**结构感知 + 语义边界**切分(对应文章 V3 思路的简化版):
优先在「第 N 条 / 标题 / 段落」边界处下刀,装不下再退到句子边界,
overlap 也对齐到完整句子,尽量不把一句话拦腰切断。
对应文章:https://www.wsxdmx.com/projects/rag-system/c/03-chunking
"""

import re
from dataclasses import dataclass, field

from .loader import LoadedDoc

# 结构边界:中文条款常见的「第N条 / 一、/(一)/ 1.」等;命中处优先开新块
_HEADING_RE = re.compile(
    r"(?=第[一二三四五六七八九十百零\d]+条)"  # 第一条 / 第10条
    r"|(?=^[一二三四五六七八九十]+、)"  # 一、二、
    r"|(?=^（[一二三四五六七八九十\d]+）)",  # (一)(二)
    re.MULTILINE,
)
# 句子边界:用于超长段落的二次切分,以及对齐 overlap
_SENT_RE = re.compile(r"(?<=[。!?；!?;\n])")


@dataclass
class Chunk:
    """切分后的一个文本块。"""

    text: str  # 这一块的文本
    source: str  # 来源文件名(溯源用)
    chunk_id: int  # 在所属文档内的序号
    metadata: dict = field(default_factory=dict)


def _split_units(text: str) -> list[str]:
    """先按结构边界切成「语义单元」,过长的单元再按句子切碎。"""
    units: list[str] = []
    for block in _HEADING_RE.split(text):
        block = block.strip()
        if not block:
            continue
        # 单个结构块不算太长就整体保留;太长则按句子拆成更小的单元
        if len(block) <= 1024:
            units.append(block)
        else:
            units.extend(s for s in _SENT_RE.split(block) if s.strip())
    return units


def _tail_overlap(text: str, overlap: int) -> str:
    """取一段文本结尾的 overlap 个字符,并裁齐到最近的句子边界(不带半截话)。"""
    if overlap <= 0 or len(text) <= overlap:
        return text if overlap > 0 else ""
    tail = text[-overlap:]
    # 从 tail 里找第一个句子起点,避免 overlap 以半句话开头
    m = re.search(r"[。!?；!?;\n]", tail)
    return tail[m.end():] if m else tail


def chunk_text(
    text: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    source: str = "",
) -> list[Chunk]:
    """把一段文本切成 Chunk 列表。

    Args:
        text: 待切分文本
        chunk_size: 目标块大小(字符数)
        chunk_overlap: 相邻块的重叠字符数,避免把一句话拦腰切断
        source: 文档来源(写进每个 chunk 的元数据)

    Returns:
        Chunk 列表(按出现顺序,chunk_id 从 0 递增)
    """
    chunks: list[Chunk] = []
    buf = ""  # 当前正在累积的块

    def flush() -> None:
        nonlocal buf
        if buf.strip():
            cid = len(chunks)
            chunks.append(Chunk(text=buf.strip(), source=source, chunk_id=cid, metadata={"source": source}))
        buf = ""

    for unit in _split_units(text):
        # 装得下就继续累积;装不下就先把当前块收口,再带 overlap 开新块
        if buf and len(buf) + len(unit) > chunk_size:
            prev = buf
            flush()
            buf = _tail_overlap(prev, chunk_overlap)
        buf += unit
        # 累积后仍超长(单个 unit 就很大),直接收口,避免无限增长
        while len(buf) > chunk_size:
            cut = buf[:chunk_size]
            m = list(_SENT_RE.finditer(cut))
            split_at = m[-1].end() if m else chunk_size  # 尽量在句子边界切
            cid = len(chunks)
            chunks.append(Chunk(text=buf[:split_at].strip(), source=source, chunk_id=cid, metadata={"source": source}))
            buf = _tail_overlap(buf[:split_at], chunk_overlap) + buf[split_at:]
    flush()
    return chunks


def chunk_doc(doc: LoadedDoc, chunk_size: int = 512, chunk_overlap: int = 50) -> list[Chunk]:
    """切分一篇已加载的文档(chunk_text 的便捷封装)。"""
    return chunk_text(doc.text, chunk_size=chunk_size, chunk_overlap=chunk_overlap, source=doc.source)
