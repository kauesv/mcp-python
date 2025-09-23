from settings.env_variables import EnvVariables
from logs.logging import get_logger
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from mcp.server.fastmcp import FastMCP
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl
import sys


logger = get_logger("main")

class StaticTokenVerifier(TokenVerifier):
    """Simple token verifier that checks against a static API key."""
    
    def __init__(self, token: str, client_id: str = "static-client", scopes: list[str] | None = None):
        """Initialize the static token verifier.
        
        Args:
            token: The valid API key token
            client_id: Client identifier for the token
            scopes: List of scopes granted to this token
        """
        self.valid_token = token
        self.client_id = client_id
        self.scopes = scopes or ["read", "write"]
    
    async def verify_token(self, token: str) -> AccessToken | None:
        """Verify the provided token against the static API key.
        
        Args:
            token: The token to verify
            
        Returns:
            AccessToken if valid, None otherwise
        """
        if token == self.valid_token:
            return AccessToken(
                token=token,
                client_id=self.client_id,
                scopes=self.scopes,
                expires_at=None  # No expiration for static tokens
            )
        return None

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[None]:
    """Manage application lifecycle."""
    
    # Initialize resources on startup
    logger.info(f"Starting {EnvVariables.MCP_SERVER_NAME}")

    """
    Antes do yield: executa o que deve acontecer quando o servidor inicia (exemplo: conectar ao banco, carregar cache, inicializar serviços).
    """
    try:
        yield
    finally:
        """
        Depois do yield (dentro do finally): executa o que deve acontecer quando o servidor encerra (exemplo: fechar conexões, limpar arquivos temporários).
        """

        # Cleanup on shutdown
        logger.info(f"Shutting down {EnvVariables.MCP_SERVER_NAME}")

# Create token verifier if API key is configured
token_verifier = None
auth_settings = None

token_verifier = StaticTokenVerifier(
    token=EnvVariables.MCP_API_KEY,
    client_id="mcp-client",
    scopes=["mcp:read", "mcp:write"]
)

# Configure auth settings
auth_settings = AuthSettings(
    issuer_url=AnyHttpUrl(f"http://{EnvVariables.MCP_HOST}:{EnvVariables.MCP_PORT}"),
    resource_server_url=AnyHttpUrl(f"http://{EnvVariables.MCP_HOST}:{EnvVariables.MCP_PORT}"),
    required_scopes=["mcp:read"]
)

# MCP
mcp = FastMCP(
    name=EnvVariables.MCP_SERVER_NAME,
    stateless_http=True,  # True para servidor http, para os outros sera ignorado
    lifespan=app_lifespan,
    host=EnvVariables.MCP_HOST,
    port=EnvVariables.MCP_PORT,
    auth=auth_settings,
    token_verifier=token_verifier
)

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together.
    
    Args:
        a: First number to add
        b: Second number to add
        
    Returns:
        The sum of a and b
        
    Example:
        >>> add(5, 3)
        8
    """
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


if __name__ == "__main__":
    try:
        if sys.argv[1] == "--http":
            logger.info(f"Starting MCP HTTP server on {EnvVariables.MCP_HOST}:{EnvVariables.MCP_PORT}")
            mcp.run(transport="streamable-http")
        else:
            logger.info("Starting MCP STDIO server")
            mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        sys.exit(1)
