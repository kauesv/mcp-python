from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from mcp.server.fastmcp import FastMCP
from config.env_variables import EnvVariables
from logs.logging import get_logger

logger = get_logger("lifespan")


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[None]:
    """Manage application lifecycle.
    
    Args:
        server: The FastMCP server instance
        
    Yields:
        None: Control back to the application during its lifetime
    """
    
    # Initialize resources on startup
    logger.info(f"Starting {EnvVariables.MCP_SERVER_NAME}")
    
    # Antes do yield: executa o que deve acontecer quando o servidor inicia 
    # (exemplo: conectar ao banco, carregar cache, inicializar serviços).
    try:
        yield
    finally:
        # Depois do yield (dentro do finally): executa o que deve acontecer quando o servidor encerra 
        # (exemplo: fechar conexões, limpar arquivos temporários).
        
        # Cleanup on shutdown
        logger.info(f"Shutting down {EnvVariables.MCP_SERVER_NAME}")
