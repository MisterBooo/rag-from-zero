"""答案生成模块 —— 对应文章第 9 章(带引用的答案生成)。

把检索到的上下文塞进 prompt,调 LLM 生成答案,并要求标注引用来源,
做到「有据可查、不瞎编」。对应文章:https://www.wsxdmx.com/projects/rag-system/c/09-citation
"""

from dataclasses import dataclass, field

from . import config
from .retriever import RetrievedChunk

# 系统提示:把「仅依据资料 + 标来源 + 没有就拒答」写死,是防幻觉的第一道闸(第 9 章)
_SYSTEM_PROMPT = (
    "你是严谨的保险客服助手。请严格遵守:\n"
    "1) 只能依据【参考资料】回答,资料里没有的信息,直接说「根据现有资料无法确定」,绝不编造;\n"
    "2) 在用到资料的地方,用 [编号] 标注来源(对应资料前的序号),做到有据可查;\n"
    "3) 回答简洁、用词通俗,面向没有保险背景的普通用户。"
)


@dataclass
class Answer:
    """生成的答案 + 引用来源。"""

    text: str  # 答案正文
    sources: list[str] = field(default_factory=list)  # 引用到的来源文件名


def _format_contexts(contexts: list[RetrievedChunk]) -> str:
    """把检索到的 chunk 编号排版成【参考资料】块,供 prompt 引用。"""
    blocks = []
    for i, rc in enumerate(contexts, start=1):
        blocks.append(f"[{i}] (来源:{rc.chunk.source}) {rc.chunk.text}")
    return "\n\n".join(blocks)


def build_messages(query: str, contexts: list[RetrievedChunk]) -> list[dict]:
    """构造发给 LLM 的 messages(纯函数,不发网络,便于单测 / 核查 prompt)。"""
    user = f"【参考资料】\n{_format_contexts(contexts)}\n\n【问题】\n{query}"
    return [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]


def generate(query: str, contexts: list[RetrievedChunk]) -> Answer:
    """基于检索到的上下文生成带引用的答案。

    Args:
        query: 用户问题
        contexts: 检索 / 重排后的上下文

    Returns:
        Answer:答案正文 + 来源列表
    """
    if not contexts:  # 没检索到 → 拒答,而不是让模型瞎编(第 9 章)
        return Answer(text="根据现有资料无法确定。没有检索到与该问题相关的内容。", sources=[])

    from openai import OpenAI  # 惰性导入

    client = OpenAI(api_key=config.DEEPSEEK_API_KEY, base_url=config.DEEPSEEK_BASE_URL)
    resp = client.chat.completions.create(
        model=config.LLM_MODEL,
        temperature=config.LLM_TEMPERATURE,
        messages=build_messages(query, contexts),
    )
    text = resp.choices[0].message.content or ""
    sources = sorted({rc.chunk.source for rc in contexts})
    return Answer(text=text, sources=sources)
