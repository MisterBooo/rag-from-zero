"""Embedding 模块 —— 对应文章第 4 章(Embedding 选型)。

把文本转成向量,让「意思相近」可以用「向量距离近」来衡量。
默认用 bge-m3 本地推理(中文友好、不花钱、数据不出本机)。
对应文章:https://www.wsxdmx.com/projects/rag-system/c/04-embedding
"""


class Embedder:
    """文本向量化器。封装模型加载与批量编码,下游只管调 encode。

    模型在首次需要时才加载(惰性),所以只是 import 本模块不会触发 ~2GB 下载。
    """

    def __init__(self, model_name: str = "BAAI/bge-m3") -> None:
        """记录模型名;真正的模型加载推迟到第一次 encode(惰性)。

        Args:
            model_name: HuggingFace 模型名,默认 bge-m3
        """
        self.model_name = model_name
        self._model = None  # 惰性:第一次用到才加载

    def _ensure_model(self):
        """第一次 encode 时加载模型(避免仅 import 就拉起 2GB 依赖)。"""
        if self._model is None:
            from sentence_transformers import SentenceTransformer  # 惰性导入

            self._model = SentenceTransformer(self.model_name)
        return self._model

    def encode(self, texts: list[str]) -> list[list[float]]:
        """把一批文本编码成(归一化的)向量。

        Args:
            texts: 文本列表

        Returns:
            向量列表,与输入一一对应
        """
        model = self._ensure_model()
        # normalize 后用内积/余弦都一致;tolist() 转成纯 Python,便于存进 ChromaDB
        vecs = model.encode(texts, normalize_embeddings=True)
        return [v.tolist() for v in vecs]

    def encode_query(self, query: str) -> list[float]:
        """编码单条查询(部分模型对 query 有专门指令前缀,故单独留接口)。"""
        return self.encode([query])[0]
