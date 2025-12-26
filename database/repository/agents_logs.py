from .repository import Repository
from config.env_variables import EnvVariables

class AgentsLogsRepository(Repository):

    def __init__(self, db):
        super(AgentsLogsRepository, self).__init__(db, collection_name=EnvVariables.MONGODB_COLLECTION_AGENTS_LOGS)