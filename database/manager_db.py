from database.repository.agents_logs import AgentsLogsRepository
from config.env_variables import EnvVariables
from database.connection.mongodb import MongoDBConnection

class ManagerMongoDB:
   """
   ManagerDB é a classe que gerencia as operações de banco de dados.
   """ 
   mongo_client = MongoDBConnection()
   mongo_client = mongo_client.connect()

   mongo_database = mongo_client[EnvVariables.MONGODB_DATABASE]

   agents_logs_repository = AgentsLogsRepository(db=mongo_database)
