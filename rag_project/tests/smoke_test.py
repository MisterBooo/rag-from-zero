"""零依赖冒烟测试 —— 不需要 API key、不下载任何模型、不连向量库。

它用「假的 Embedder + 内存版向量库」替换掉重型组件,但**真实地**跑:
  结构感知切分(chunker)→ 向量+BM25 双路 + RRF 融合(retriever)
  → Query 规则改写(query_processor)→ 带引用的 prompt 构造(generator)。

目的:核查整条装配链路的逻辑是否正确——这是项目里除了「模型推理 / API 调用」
之外的全部代码。CI 里跑它,几秒钟就能确认代码没写错。

用法:python tests/smoke_test.py   (仅需 python-dotenv;不需要其它依赖)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.chunker import Chunk, chunk_text
from src.generator import build_messages, generate
from src.query_processor import process_query
from src.retriever import RetrievedChunk, Retriever


# ─── 用「假组件」替换重型依赖,只为验证装配逻辑(鸭子类型,接口一致即可) ───
class FakeEmbedder:
    """把文本映射成一个固定维度的「词袋计数」向量,完全本地、零依赖。"""

    DIM = 64

    def _vec(self, text: str) -> list[float]:
        v = [0.0] * self.DIM
        for ch in text:
            v[ord(ch) % self.DIM] += 1.0
        return v

    def encode(self, texts):
        return [self._vec(t) for t in texts]

    def encode_query(self, query):
        return self._vec(query)


class FakeStore:
    """内存版向量库:用余弦相似度返回最近的 chunk,替代 ChromaDB。"""

    def __init__(self, chunks, embedder):
        self.chunks = chunks
        self.vecs = embedder.encode([c.text for c in chunks])

    @staticmethod
    def _cos(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        na = sum(x * x for x in a) ** 0.5
        nb = sum(y * y for y in b) ** 0.5
        return dot / (na * nb) if na and nb else 0.0

    def query(self, query_embedding, top_k=5):
        scored = sorted(
            range(len(self.chunks)),
            key=lambda i: self._cos(query_embedding, self.vecs[i]),
            reverse=True,
        )
        return [self.chunks[i] for i in scored[:top_k]]

    def all_chunks(self):
        return self.chunks


# ─── 测试用例 ─────────────────────────────────────────────────────
DOC = (
    "第一条 责任范围 本保险承保意外伤害导致的身故或残疾。"
    "第二条 责任免除 下列情形不承担给付责任:核爆炸、核辐射或核污染;酒后驾驶。"
    "第三条 等待期 本产品等待期为 90 天,自合同生效日起算,意外伤害不受等待期限制。"
    "第四条 犹豫期 本产品犹豫期为 15 天,犹豫期内可无理由退保并全额退还保费。"
)

PASS, FAIL = "✅", "❌"
failures = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global failures
    print(f"  {PASS if cond else FAIL} {name}" + (f"  — {detail}" if detail and not cond else ""))
    if not cond:
        failures += 1


def main() -> None:
    print("== 1. 切分(chunker)==")
    chunks = chunk_text(DOC, chunk_size=60, chunk_overlap=15, source="policy.pdf")
    check("切出多个 chunk", len(chunks) >= 3, f"实际 {len(chunks)}")
    check("每个 chunk 不超目标太多", all(len(c.text) <= 90 for c in chunks))
    check("chunk 带 source 元数据", all(c.source == "policy.pdf" for c in chunks))
    check("在条款边界附近下刀", any(c.text.startswith("第") for c in chunks))

    print("== 2. 混合检索 + RRF(retriever)==")
    embedder = FakeEmbedder()
    store = FakeStore(chunks, embedder)
    retriever = Retriever(store, embedder, chunks)
    hits = retriever.retrieve("核辐射保不保", top_k=3, top_n=10)
    check("检索有结果", len(hits) > 0)
    check("命中『核辐射』所在 chunk", any("核辐射" in h.chunk.text for h in hits))
    check("结果按 RRF 分降序", all(hits[i].score >= hits[i + 1].score for i in range(len(hits) - 1)))

    print("== 3. Query 改写(规则兜底,无 key)==")
    pq = process_query("请问一下等待期是多少天呀?")
    check("去掉了口语词", "请问" not in pq.rewritten and "呀" not in pq.rewritten, pq.rewritten)
    check("保留了核心词", "等待期" in pq.rewritten, pq.rewritten)
    check("all_queries 含改写", pq.rewritten in pq.all_queries())

    print("== 4. 带引用的 prompt 构造(generator)==")
    ctx = [RetrievedChunk(chunk=c, score=1.0) for c in chunks[:2]]
    msgs = build_messages("等待期多久", ctx)
    sys_text, user_text = msgs[0]["content"], msgs[1]["content"]
    check("system 强约束『仅依据资料』", "只能依据" in sys_text)
    check("user 含编号 [1]", "[1]" in user_text)
    check("user 含来源标注", "来源:policy.pdf" in user_text)

    print("== 5. 拒答(无上下文不调用 API)==")
    ans = generate("火星保险保不保", [])
    check("空上下文 → 拒答而非编造", "无法确定" in ans.text and ans.sources == [])

    print()
    if failures:
        print(f"{FAIL} 冒烟测试未通过:{failures} 处失败")
        sys.exit(1)
    print(f"{PASS} 全部通过:装配链路逻辑正确(切分 / 检索融合 / 改写 / 引用 / 拒答)")


if __name__ == "__main__":
    main()
