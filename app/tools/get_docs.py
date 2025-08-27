from app.services.search_web import SearchWeb
from app.services.fetch_url import FetchUrl


docs_urls = {
    "langchain": "python.langchain.com/docs",
    "llama-index": "docs.llamaindex.ai/en/stable",
    "openai": "platform.openai.com/docs",
}

# As docstrings são usadas pelos agentes para entender o que cada ferramenta faz.

async def get_docs(query: str, library: str):
  """
  Busca a documentação mais recente para uma determinada consulta e biblioteca.
  Suporta langchain, openai e llama-index.

  Argumentos:
    query: A consulta a ser pesquisada (ex: "Chroma DB")
    library: A biblioteca na qual pesquisar (ex: "langchain")

  Retorna:
    Texto extraído da documentação
  """
  if library not in docs_urls:
    raise ValueError(f"Library {library} not supported by this tool")
  
  query = f"site:{docs_urls[library]} {query}"
  results = await SearchWeb.execute({"query": query})
  if len(results["organic"]) == 0:
    return "No results found"
  
  text = ""
  for result in results["organic"]:
    text += await FetchUrl.execute({"url": result["link"]})
  return text