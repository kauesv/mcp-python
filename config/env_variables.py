from os import environ, path
from dotenv import load_dotenv


env_file_path = path.join(path.dirname(path.abspath(__file__)), ".env")
if path.exists(env_file_path):
    load_dotenv(dotenv_path=env_file_path)
else:
    load_dotenv()

class EnvVariables:
    #   MCP
    MCP_SERVER_NAME = environ.get("MCP_SERVER_NAME", "mcp-python-server")
    MCP_SERVER_VERSION = environ.get("MCP_SERVER_VERSION", "1.0.0")
    MCP_LOG_LEVEL = environ.get('MCP_LOG_LEVEL')
    MCP_SERVER_USER_AGENT = environ.get(
        "MCP_SERVER_USER_AGENT", f"{MCP_SERVER_NAME}/{MCP_SERVER_VERSION}"
    )
    MCP_HOST = environ.get('MCP_HOST', "localhost")
    MCP_PORT = environ.get('MCP_PORT', 2000)
    MCP_API_KEY = environ.get('MCP_API_KEY')

    #   Diretórios
    BASE_PATH = environ.get('BASE_PATH')
    LOG_PATH = environ.get('LOG_PATH')