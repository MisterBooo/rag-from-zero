"""
RAG 教程第 8 章 - 零依赖多轮记忆 demo

不需要装任何库,直接 python3 memory_demo.py 就能跑。
目的:亲眼看到"没有记忆,多轮里的'它'就无解;有了记忆 + 滑动窗口 + 指代补全,
      模型才能接住上一轮的话"。

对应文章:https://www.wsxdmx.com/projects/rag-system/c/08-memory
"""

# 知识库就用一个字典:键是"产品+问题",值是答案(真实系统是第 3~6 章那套检索)
KB = {
    ("重疾险", "犹豫期"): "重疾险犹豫期为 15 天,自签收次日起算。",
    ("重疾险", "退"): "重疾险在犹豫期内可全额退保,过了犹豫期退保只退现金价值。",
    ("意外险", "犹豫期"): "意外险通常无犹豫期或仅几天,以条款为准。",
}

PRODUCTS = ["重疾险", "意外险", "年金险"]   # 系统认识的实体


class ConversationMemory:
    """最朴素的对话记忆:滑动窗口保留最近几轮 + 更早的压成一句摘要。"""

    def __init__(self, window: int = 2):
        self.window = window      # 滑动窗口:只在上下文里保留最近 window 轮
        self.history: list[tuple[str, str]] = []   # [(用户问, 助手答), ...]
        self.summary = ""         # 挤出窗口的旧对话,压成摘要(真实系统用 LLM 概括)

    def add(self, user: str, bot: str):
        self.history.append((user, bot))           # 新一轮先进历史
        while len(self.history) > self.window:      # 超出窗口 → 最旧一轮挤出
            old_user, _ = self.history.pop(0)
            self.summary += f"用户先前问过「{old_user}」;"   # 朴素"摘要"

    def context(self) -> str:
        """拼出要喂给模型的上下文:更早摘要 + 窗口内的逐轮对话。"""
        parts = []
        if self.summary:
            parts.append(f"[更早摘要] {self.summary}")
        for u, b in self.history:
            parts.append(f"用户:{u}\n助手:{b}")
        return "\n".join(parts) if parts else "(空)"


def last_entity(mem: ConversationMemory):
    """从最近的历史里,找出最后提到的那个产品(给指代消解用)。"""
    found = None
    for u, _ in mem.history:
        for p in PRODUCTS:
            if p in u:
                found = p          # 一直覆盖,留下"最近一次提到的"
    return found


def resolve(query: str, mem: ConversationMemory) -> str:
    """朴素指代消解:把'它'换成最近提到的产品,让问题能独立检索。"""
    ent = last_entity(mem)
    if "它" in query and ent:
        return query.replace("它", ent)
    return query


def answer(query: str) -> str:
    """查知识库:命中产品+关键词就返回答案,否则算检索失败。"""
    for (prod, kw), text in KB.items():
        if prod in query and kw in query:
            return text
    return "【没接住】问题里没有明确的产品,检索失败"


if __name__ == "__main__":
    mem = ConversationMemory(window=2)

    print("=== 带记忆 + 指代消解 ===")
    q1 = "重疾险的犹豫期多久?"
    a1 = answer(q1)
    print(f"轮1 用户:{q1}\n     助手:{a1}\n")
    mem.add(q1, a1)

    q2 = "那它过了还能退吗?"            # "它"指上一轮的重疾险
    resolved = resolve(q2, mem)         # 用记忆把"它"补全
    a2 = answer(resolved)
    print(f"轮2 用户原话:{q2}")
    print(f"     补全后 :{resolved}")
    print(f"     助手   :{a2}\n")

    print("=== 对照:不带记忆,直接拿原话检索 ===")
    print(f"轮2 用户:{q2}")
    print(f"     助手:{answer(q2)}   <- '它'无法解析,检索失败")
