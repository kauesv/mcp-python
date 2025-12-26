from logs.logging import get_logger
from logs.agents import agents_logger
from datetime import datetime
from typing import Optional, Dict, Any, List

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
    
    @mcp.tool()
    def log_agents_interaction(
        project_name: str,
        agent_name: str,
        interaction_type: str,
        user_input: Optional[str] = None,
        agent_response: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ) -> bool:
        """Log an AI agent interaction to MongoDB.
        
        Args:
            project_name: Human-readable name of the project
            agent_name: Human-readable name of the agent
            interaction_type: Type of interaction (e.g., 'chat', 'task', 'query')
            user_input: User's input to the agent
            agent_response: Agent's response
            metadata: Additional metadata about the interaction
            session_id: Session identifier for grouping related interactions
            
        Returns:
            bool: True if log was successful, False otherwise
            
        Example:
            >>> log_agents_interaction(
            ...     project_name="Customer Support",
            ...     agent_name="Customer Support Bot",
            ...     interaction_type="chat",
            ...     user_input="How can I reset my password?",
            ...     agent_response="You can reset your password by clicking...",
            ...     metadata={"user_id": "123"},
            ...     session_id="session_123"
            ... )
            True
        """
        try:            
            success = agents_logger.log_agent_interaction(
                project_name=project_name,
                agent_name=agent_name,
                interaction_type=interaction_type,
                user_input=user_input,
                agent_response=agent_response,
                metadata=metadata,
                session_id=session_id
            )
            
            if success:
                logger.info(f"Successfully logged interaction for agent {agent_name}")
            else:
                logger.error(f"Failed to log interaction for agent {agent_name}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error logging AI agent interaction: {e}")
            return False

    @mcp.tool()
    def get_agents_logs(
        agent_name: Optional[str] = None,
        session_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Retrieve AI agent logs from MongoDB with optional filtering.
        
        Args:
            agent_name: Filter by specific agent name
            session_id: Filter by specific session ID
            start_date: Filter logs from this date onwards (ISO format: YYYY-MM-DD)
            end_date: Filter logs up to this date (ISO format: YYYY-MM-DD)
            limit: Maximum number of logs to return (default: 100)
            
        Returns:
            List[Dict[str, Any]]: List of log entries
            
        Example:
            >>> get_agents_logs(
            ...     agent_name="agent_001",
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31",
            ...     limit=50
            ... )
            [{"agent_name": "agent_001", "interaction_type": "chat", ...}, ...]
        """
        try:
            # Parse date strings if provided
            start_dt = None
            end_dt = None
            
            if start_date:
                try:
                    start_dt = datetime.fromisoformat(start_date)
                except ValueError:
                    logger.error(f"Invalid start_date format: {start_date}. Use YYYY-MM-DD format.")
                    return []
            
            if end_date:
                try:
                    end_dt = datetime.fromisoformat(end_date)
                except ValueError:
                    logger.error(f"Invalid end_date format: {end_date}. Use YYYY-MM-DD format.")
                    return []
            
            logs = agents_logger.get_agent_logs(
                agent_name=agent_name,
                session_id=session_id,
                start_date=start_dt,
                end_date=end_dt,
                limit=limit
            )
            
            logger.info(f"Retrieved {len(logs)} logs for agent {agent_name}")
            return logs
            
        except Exception as e:
            logger.error(f"Error retrieving AI agent logs: {e}")
            return []
    
    @mcp.tool()
    def get_agents_statistics(
        agent_name: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get statistics for a specific AI agent from MongoDB.
        
        Args:
            agent_name: Agent name to get statistics for
            start_date: Start date for statistics period (ISO format: YYYY-MM-DD)
            end_date: End date for statistics period (ISO format: YYYY-MM-DD)
            
        Returns:
            Dict[str, Any]: Agent statistics including interaction counts, task statuses, etc.
            
        Example:
            >>> get_agents_statistics(
            ...     agent_name="agent_001",
            ...     start_date="2024-01-01",
            ...     end_date="2024-01-31"
            ... )
            {
                "agent_name": "agent_001",
                "total_interactions": 150,
                "interaction_types": {"chat": 100, "task": 50},
                "task_statuses": {"completed": 45, "failed": 5},
                "average_execution_time_ms": 2500.0
            }
        """
        try:
            # Parse date strings if provided
            start_dt = None
            end_dt = None
            
            if start_date:
                try:
                    start_dt = datetime.fromisoformat(start_date)
                except ValueError:
                    logger.error(f"Invalid start_date format: {start_date}. Use YYYY-MM-DD format.")
                    return {}
            
            if end_date:
                try:
                    end_dt = datetime.fromisoformat(end_date)
                except ValueError:
                    logger.error(f"Invalid end_date format: {end_date}. Use YYYY-MM-DD format.")
                    return {}
            
            statistics = agents_logger.get_agent_statistics(
                agent_name=agent_name,
                start_date=start_dt,
                end_date=end_dt
            )
            
            logger.info(f"Retrieved statistics for agent {agent_name}")
            return statistics
            
        except Exception as e:
            logger.error(f"Error retrieving AI agent statistics: {e}")
            return {}
    
    logger.info("Tools registered successfully")
