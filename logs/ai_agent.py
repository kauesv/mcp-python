"""
AI Agent Logger Module

Handles logging of AI agent activities to MongoDB database.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pymongo.errors import PyMongoError
from logs.logging import get_logger
from database.manager_db import ManagerMongoDB

logger = get_logger("ai_agent_logger")


class AIAgentLogger:
    """Logger for AI agent activities and interactions."""
    
    def __init__(self):
        """Initialize the AI Agent Logger."""
        self.collection = ManagerMongoDB.fluxo_husky_repository.collection
    
    def log_agent_interaction(
        self,
        project_name: str,
        agent_name: str,
        interaction_type: str,
        user_input: Optional[str] = None,
        agent_response: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> bool:
        """Log an AI agent interaction.
        
        Args:
            agent_name: Human-readable name of the agent
            interaction_type: Type of interaction (e.g., 'chat', 'task', 'query')
            user_input: User's input to the agent
            agent_response: Agent's response
            metadata: Additional metadata about the interaction
            session_id: Session identifier for grouping related interactions
            timestamp: When the interaction occurred (defaults to now)
            
        Returns:
            bool: True if log was successful, False otherwise
        """
        try:
            log_entry = {
                "project_name": project_name,
                "agent_name": agent_name,
                "interaction_type": interaction_type,
                "user_input": user_input,
                "agent_response": agent_response,
                "metadata": metadata or {},
                "session_id": session_id,
                "timestamp": timestamp or datetime.now(),
                "created_at": datetime.now()
            }
            
            result = self.collection.insert_one(log_entry)
            logger.debug(f"Logged interaction for agent {agent_name}: {result.inserted_id}")
            return True
            
        except PyMongoError as e:
            logger.error(f"Failed to log agent interaction: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error logging agent interaction: {e}")
            return False
    
    def get_agent_logs(
        self,
        agent_name: Optional[str] = None,
        session_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Retrieve agent logs with optional filtering.
        
        Args:
            agent_name: Filter by specific agent name
            session_id: Filter by specific session ID
            start_date: Filter logs from this date onwards
            end_date: Filter logs up to this date
            limit: Maximum number of logs to return
            
        Returns:
            List[Dict[str, Any]]: List of log entries
        """
        try:
            query = {}
            
            if agent_name:
                query["agent_name"] = agent_name
            if session_id:
                query["session_id"] = session_id
            if start_date or end_date:
                query["timestamp"] = {}
                if start_date:
                    query["timestamp"]["$gte"] = start_date
                if end_date:
                    query["timestamp"]["$lte"] = end_date
            
            cursor = self.collection.find(query).sort("timestamp", -1).limit(limit)
            logs = list(cursor)
            
            logger.debug(f"Retrieved {len(logs)} logs for agent {agent_name}")
            return logs
            
        except PyMongoError as e:
            logger.error(f"Failed to retrieve agent logs: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error retrieving agent logs: {e}")
            return []
    
    def get_agent_statistics(
        self,
        agent_name: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get statistics for a specific agent.
        
        Args:
            agent_name: Agent name to get statistics for
            start_date: Start date for statistics period
            end_date: End date for statistics period
            
        Returns:
            Dict[str, Any]: Agent statistics
        """
        try:
            query = {"agent_name": agent_name}
            
            if start_date or end_date:
                query["timestamp"] = {}
                if start_date:
                    query["timestamp"]["$gte"] = start_date
                if end_date:
                    query["timestamp"]["$lte"] = end_date
            
            # Count total interactions
            total_interactions = self.collection.count_documents(query)
            
            # Count by interaction type
            interaction_types = list(self.collection.aggregate([
                {"$match": query},
                {"$group": {"_id": "$interaction_type", "count": {"$sum": 1}}}
            ]))
            
            # Count by status (for tasks)
            task_statuses = list(self.collection.aggregate([
                {"$match": {**query, "status": {"$exists": True}}},
                {"$group": {"_id": "$status", "count": {"$sum": 1}}}
            ]))
            
            # Get average execution time
            avg_execution_time = self.collection.aggregate([
                {"$match": {**query, "execution_time_ms": {"$exists": True}}},
                {"$group": {"_id": None, "avg_time": {"$avg": "$execution_time_ms"}}}
            ])
            avg_time_result = list(avg_execution_time)
            avg_execution_time_ms = avg_time_result[0]["avg_time"] if avg_time_result else None
            
            statistics = {
                "agent_name": agent_name,
                "total_interactions": total_interactions,
                "interaction_types": {item["_id"]: item["count"] for item in interaction_types},
                "task_statuses": {item["_id"]: item["count"] for item in task_statuses},
                "average_execution_time_ms": avg_execution_time_ms,
                "period": {
                    "start_date": start_date,
                    "end_date": end_date
                }
            }
            
            logger.debug(f"Retrieved statistics for agent {agent_name}")
            return statistics
            
        except PyMongoError as e:
            logger.error(f"Failed to get agent statistics: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error getting agent statistics: {e}")
            return {}


# Global AI Agent Logger instance
ai_agent_logger = AIAgentLogger()
