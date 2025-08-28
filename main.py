from mcp.server.fastmcp import FastMCP
from app.settings import VariablesMCPPython
from app.tools.get_docs import get_docs
from app.tools.text_stats import text_stats
from app.tools.unit_converter import convert_units


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
    description="Busca a documentação mais recente para uma determinada consulta e biblioteca."
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


@mcp.tool(
    name="text_stats",
    description="Calcula estatísticas básicas de um texto fornecido."
)
async def text_stats_tool(text: str):
    """
    Calcula estatísticas básicas de um texto fornecido.

    Argumentos:
        text: O texto para analisar

    Retorna:
        Dicionário com estatísticas do texto (contagem de caracteres, palavras, linhas, etc.)
    """
    return await text_stats(text)


@mcp.tool(
    name="convert_units",
    description="Converte valores entre diferentes unidades de medida."
)
async def convert_units_tool(value: float, from_unit: str, to_unit: str):
    """
    Converte valores entre diferentes unidades de medida.

    Argumentos:
        value: O valor numérico para converter
        from_unit: A unidade de origem (ex: "km", "miles", "kg", "lbs")
        to_unit: A unidade de destino (ex: "m", "km", "g", "oz")

    Retorna:
        Dicionário com o valor convertido e informações sobre a conversão
    """
    return await convert_units(value, from_unit, to_unit)

# Run
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        print(f"🚀 Iniciando servidor MCP HTTP em {VariablesMCPPython.host}:{VariablesMCPPython.port}")
        mcp.run(transport="streamable-http")
    else:
        print("🔌 Iniciando servidor MCP STDIO")
        mcp.run(transport="stdio")
