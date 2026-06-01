"""集中配置管理:所有可调参数、路径、key 都在这里,改一处即可。

约定:
- 敏感信息(API key)只从环境变量 / .env 读,绝不写死在代码里。
- 路径一律基于本文件位置推导,不依赖运行时的当前目录,从哪儿调都不会错。
"""

import os
from pathlib import Path

# 显式指向 rag_project/.env,无论从哪个目录运行脚本都能找到
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# python-dotenv 只是「从 .env 文件读 key」的便利;没装也不影响——直接读环境变量即可。
# (这样冒烟测试 / CI 可以零依赖跑起来。)
try:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env")
except ModuleNotFoundError:
    pass

# ─── 路径 ─────────────────────────────────────────────────────────
DATA_DIR = PROJECT_ROOT / "data" / "sample_docs"
CHROMA_DIR = PROJECT_ROOT / os.getenv("CHROMA_PERSIST_DIR", "chroma_data")

# ─── LLM ──────────────────────────────────────────────────────────
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))

# ─── Embedding / 重排模型 ─────────────────────────────────────────
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
RERANKER_MODEL = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-v2-m3")

# ─── 切分 / 检索 / 重排默认值(脚本可覆盖) ────────────────────────
CHUNK_SIZE = 512  # 每个 chunk 目标字符数(第 3 章)
CHUNK_OVERLAP = 50  # 相邻 chunk 重叠字符数,避免把一句话拦腰切断
RETRIEVE_TOP_N = 20  # 召回候选池大小:双路各取前 N 再融合(第 5 章)
RERANK_TOP_K = 5  # 重排后保留、最终喂给 LLM 的条数(第 6 章)
TOP_K = 5  # 不开重排时,检索直接返回的条数

# 开关:没装重型模型 / 想先跑通时,可在 .env 里关掉(设为 0 / false)
USE_RERANK = os.getenv("USE_RERANK", "1").lower() not in ("0", "false", "no")
USE_QUERY_REWRITE = os.getenv("USE_QUERY_REWRITE", "1").lower() not in ("0", "false", "no")


def validate_config() -> None:
    """启动时校验关键配置,缺什么提前给出清晰的中文提示,而不是等调用时报一堆栈。"""
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY.startswith("sk-your-key"):
        raise ValueError(
            "\n❌ 缺少 DEEPSEEK_API_KEY\n"
            "   1) 复制配置模板:cp .env.example .env\n"
            "   2) 编辑 .env,填入你的 DeepSeek API key\n"
            "   3) 申请地址:https://platform.deepseek.com/api_keys\n"
        )
