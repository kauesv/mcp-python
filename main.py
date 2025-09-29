"""
MCP Python Server - Main Entry Point

A modular MCP (Model Context Protocol) server implementation with authentication,
tools, resources, and prompts support.
"""

import sys
from config.server_config import create_mcp_server
from config.env_variables import EnvVariables
from handlers.tools import register_tools
from handlers.resources import register_resources
from handlers.prompts import register_prompts
from logs.logging import get_logger

logger = get_logger("main")


def setup_server():
    """Setup and configure the MCP server with all handlers.
    
    Returns:
        FastMCP: Configured server ready to run
    """
    # Create the MCP server
    mcp = create_mcp_server()
    
    # Register all handlers
    register_tools(mcp)
    register_resources(mcp)
    register_prompts(mcp)
    
    logger.info("MCP server setup completed successfully")
    return mcp


# Create the MCP server instance as a global variable
# This is required for the MCP dev command to find the server object
mcp = setup_server()

def main():
    """Main entry point for the MCP server."""
    try:
        # Determine transport mode
        if len(sys.argv) > 1 and sys.argv[1] == "--http":
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


if __name__ == "__main__":
    main()