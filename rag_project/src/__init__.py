"""RAG From Zero · 端到端项目核心包。

各模块对应教程章节(loader/chunker→第3章,embedder→第4章,vectorstore/retriever→第5章,
reranker→第6章,query_processor→第7章,generator→第9章),由 pipeline 串成完整链路。
详见 rag_project/README.md 的「对应文章」表。

重型依赖(chromadb / sentence-transformers / openai)均在用到时才惰性导入,
所以仅 import 本包不会触发模型下载或要求 API key。
"""
