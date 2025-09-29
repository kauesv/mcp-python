"""
MongoDB Configuration Module

Handles MongoDB connection setup and configuration for AI agent logging.
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config.env_variables import EnvVariables
from logs.logging import get_logger

logger = get_logger("mongodb_config")


class MongoDBConnection:
    """MongoDB connection manager."""
    
    def __init__(self):
        self.uri = EnvVariables.MONGODB_URI

    def connect(self):
        """Establish connection to MongoDB."""
        self._client = MongoClient(self.uri)

        try:
            self._client.admin.command('ping')
            logger.info("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")

        return self._client
