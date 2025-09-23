from logs.logging import get_logger

logger = get_logger("prompts")


def register_prompts(mcp):
    """Register all MCP prompts with the server.
    
    Args:
        mcp: The FastMCP server instance
    """
    
    @mcp.prompt()
    def greet_user(name: str, style: str = "friendly") -> str:
        """Generate a greeting prompt.
        
        Args:
            name: The name of the person to greet
            style: The style of greeting (friendly, formal, casual)
            
        Returns:
            A greeting prompt message
        """
        styles = {
            "friendly": "Please write a warm, friendly greeting",
            "formal": "Please write a formal, professional greeting",
            "casual": "Please write a casual, relaxed greeting",
        }

        prompt = f"{styles.get(style, styles['friendly'])} for someone named {name}."
        logger.debug(f"Generated prompt for {name} with style '{style}'")
        return prompt
    
    logger.info("Prompts registered successfully")
