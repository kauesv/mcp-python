from mcp.server.fastmcp import FastMCP
from app.settings import VariablesMCPPython
from app.tools.get_docs import get_docs


# MCP
mcp = FastMCP(
    name=VariablesMCPPython.server_name,
    stateless_http=VariablesMCPPython.stateless_http,
    host=VariablesMCPPython.host,
    port=VariablesMCPPython.port
)

# Tools
@mcp.tool(
    name="get_docs",
    description="Busca a documentação mais recente para uma determinada consulta e biblioteca.",
    structured_output=True
)
async def get_docs_tool(query: str, library: str):
    """
    Busca a documentação mais recente para uma determinada consulta e biblioteca.
    Suporta langchain, openai e llama-index.

    Argumentos:
        query: A consulta a ser pesquisada (ex: "Chroma DB")
        library: A biblioteca na qual pesquisar (ex: "langchain")

    Retorna:
        Texto extraído da documentação
    """
    return await get_docs(query, library)

# Run
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        print(f"🚀 Iniciando servidor MCP HTTP em {VariablesMCPPython.host}:{VariablesMCPPython.port}")
        mcp.run(transport="streamable-http")
    else:
        print("🔌 Iniciando servidor MCP STDIO")
        mcp.run(transport="stdio")
