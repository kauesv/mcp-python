from logs.logging import get_logger

logger = get_logger("tools")


def register_tools(mcp):
    """Register all MCP tools with the server.
    
    Args:
        mcp: The FastMCP server instance
    """
    
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
        result = a + b
        logger.debug(f"Adding {a} + {b} = {result}")
        return result
    
    logger.info("Tools registered successfully")
