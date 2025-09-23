from logs.logging import get_logger

logger = get_logger("resources")


def register_resources(mcp):
    """Register all MCP resources with the server.
    
    Args:
        mcp: The FastMCP server instance
    """
    
    @mcp.resource("greeting://{name}")
    def get_greeting(name: str) -> str:
        """Get a personalized greeting.
        
        Args:
            name: The name of the person to greet
            
        Returns:
            A personalized greeting message
        """
        greeting = f"Hello, {name}!"
        logger.debug(f"Generated greeting: {greeting}")
        return greeting
    
    logger.info("Resources registered successfully")
