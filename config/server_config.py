from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl
from config.env_variables import EnvVariables
from auth.token_verifier import StaticTokenVerifier
from core.lifespan import app_lifespan
from logs.logging import get_logger

logger = get_logger("server_config")


def create_mcp_server() -> FastMCP:
    """
    Creates and configures the FastMCP server with authentication and settings.
    
    Returns:
        FastMCP: Configured MCP server instance
    """
    # Create token verifier
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

    # Create MCP server
    mcp = FastMCP(
        name=EnvVariables.MCP_SERVER_NAME,
        stateless_http=True,  # True para servidor http, para os outros sera ignorado
        lifespan=app_lifespan,
        host=EnvVariables.MCP_HOST,
        port=EnvVariables.MCP_PORT,
        auth=auth_settings,
        token_verifier=token_verifier
    )
    
    logger.info(f"MCP server '{EnvVariables.MCP_SERVER_NAME}' configured successfully")
    return mcp
