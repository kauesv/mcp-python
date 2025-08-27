from typing import Optional
from os import environ
from dotenv import load_dotenv, find_dotenv
from typing import Dict, Any

path_dot_env = find_dotenv(".env")
load_dotenv(dotenv_path=path_dot_env)


class VariablesMCPPython:
    """
    Configurações do servidor MCP Python.
    """

    server_name: str = environ.get("MCP_SERVER_NAME", "mcp-python-server")
    server_version: str = environ.get("MCP_SERVER_VERSION", "1.0.0")
    server_user_agent: str = environ.get(
        "MCP_SERVER_USER_AGENT", f"{server_name}/{server_version}"
    )

    stateless_http: bool = environ.get("STATLESSL_HTTP", "False").lower() == "true"

    # HTTP Server settings
    host: str = environ.get("MCP_HOST", "localhost")
    port: int = int(environ.get("MCP_PORT", 8000))

    # API settings
    serper_api_key: str = environ.get("SERPER_API_KEY", "")
    serper_url: str = environ.get("SERPER_URL", "https://google.serper.dev/search")

    # Logging settings
    log_level: str = environ.get("MCP_LOG_LEVEL", "INFO")
    log_format: str = environ.get(
        "MCP_LOG_FORMAT", "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
    )
    log_file: Optional[str] = environ.get("MCP_LOG_FILE", None)
    default_log_file: str = environ.get(
        "DEFAULT_LOG_FILE", "logs/logs_{datetime.now().strftime('%Y-%m-%d')}.log"
    )
    log_path: str = environ.get("LOG_PATH", "mcp/data/logs")

    # Tool settings
    max_tool_execution_time: int = int(environ.get("MCP_MAX_TOOL_EXECUTION_TIME", 30))
    enable_tool_validation: bool = environ.get("MCP_ENABLE_TOOL_VALIDATION", "true").lower() == "true"

    # Resource settings
    max_resource_size: int = int(environ.get("MCP_MAX_RESOURCE_SIZE", 1024 * 1024))  # 1MB
    enable_resource_caching: bool = environ.get("MCP_ENABLE_RESOURCE_CACHING", "true").lower() == "true"

    # Security settings
    enable_input_validation: bool = environ.get("MCP_ENABLE_INPUT_VALIDATION", "true").lower() == "true"
    max_input_length: int = int(environ.get("MCP_MAX_INPUT_LENGTH", 10000))



def get_mcp_server_config() -> Dict[str, Any]:
    """
    Retorna a configuração do servidor MCP.
    """
    return {
        "name": VariablesMCPPython.server_name,
        "version": VariablesMCPPython.server_version,
        "description": "MCP Python Server com ferramentas personalizadas para busca web e documentação",
        "capabilities": {
            "tools": {
                "listChanged": False,
                "listNotChanged": False,
            },
            "resources": {
                "listChanged": False,
                "listNotChanged": False,
            },
            "prompts": {
                "listChanged": False,
                "listNotChanged": False,
            },
        },
    }