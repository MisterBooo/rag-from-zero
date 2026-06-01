"""Query 理解与改写模块 —— 对应文章第 7 章。

用户的原始问题往往口语、含糊、缺关键词。先做改写 / 扩展,再去检索,
召回率能明显提升。对应文章:https://www.wsxdmx.com/projects/rag-system/c/07-query-understanding

两条路径:
- 有 DeepSeek key 且开启改写 → 调 LLM 做规范化改写 + 同义扩展(效果好);
- 没 key / 关闭 → 规则兜底:去掉口语词(保证无 key 也能跑通,不崩)。
"""

import json
import re
from dataclasses import dataclass, field

from . import config

# 口语 / 无意义词,规则兜底时删掉
_FILLER = ["请问", "麻烦问下", "我想问一下", "想了解一下", "一下", "请", "啊", "呢", "呀", "吧", "哈"]


@dataclass
class ProcessedQuery:
    """处理后的查询:一条规范化主查询 + 若干扩展查询。"""

    original: str  # 用户原始问题
    rewritten: str  # 改写后的规范查询
    expansions: list[str] = field(default_factory=list)  # 同义 / 多角度扩展查询

    def all_queries(self) -> list[str]:
        """主查询 + 扩展去重,供检索逐个尝试。"""
        seen, out = set(), []
        for q in [self.rewritten, *self.expansions, self.original]:
            q = q.strip()
            if q and q not in seen:
                seen.add(q)
                out.append(q)
        return out


def _rule_rewrite(query: str) -> str:
    """规则兜底改写:删口语词、去首尾标点空白。"""
    q = query
    for f in _FILLER:
        q = q.replace(f, "")
    return q.strip(" ?？!!。,,") or query.strip()


def _llm_rewrite(query: str) -> ProcessedQuery:
    """调 DeepSeek 做改写 + 扩展,要求输出 JSON,解析失败则回退规则版。"""
    from openai import OpenAI  # 惰性导入

    client = OpenAI(api_key=config.DEEPSEEK_API_KEY, base_url=config.DEEPSEEK_BASE_URL)
    prompt = (
        "你是检索查询改写器。把用户问题改写成更书面、更贴近文档表达的一句话,"
        "并给出 1-3 个同义/不同角度的扩展查询(用于提高召回)。\n"
        '只输出 JSON,格式:{"rewritten": "...", "expansions": ["...", "..."]}\n\n'
        f"用户问题:{query}"
    )
    resp = client.chat.completions.create(
        model=config.LLM_MODEL,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.choices[0].message.content or ""
    m = re.search(r"\{.*\}", raw, re.S)  # 容忍模型多输出的解释文字
    try:
        data = json.loads(m.group(0)) if m else {}
        rewritten = (data.get("rewritten") or "").strip() or _rule_rewrite(query)
        expansions = [e.strip() for e in data.get("expansions", []) if e and e.strip()]
        return ProcessedQuery(original=query, rewritten=rewritten, expansions=expansions[:3])
    except (ValueError, AttributeError):
        return ProcessedQuery(original=query, rewritten=_rule_rewrite(query))


def process_query(query: str) -> ProcessedQuery:
    """对原始查询做理解、改写与扩展。

    Args:
        query: 用户原始问题

    Returns:
        ProcessedQuery
    """
    has_key = config.DEEPSEEK_API_KEY and not config.DEEPSEEK_API_KEY.startswith("sk-your-key")
    if config.USE_QUERY_REWRITE and has_key:
        try:
            return _llm_rewrite(query)
        except Exception:
            pass  # 网络/额度问题不该让整个问答挂掉,降级到规则版
    return ProcessedQuery(original=query, rewritten=_rule_rewrite(query))
