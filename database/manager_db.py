from database.repository.fluxo_husky import FluxoHuskyRepository
from config.env_variables import EnvVariables
from database.connection.mongodb import MongoDBConnection

class ManagerMongoDB:
   """
   ManagerDB é a classe que gerencia as operações de banco de dados.
   """ 
   mongo_client = MongoDBConnection()
   mongo_client = mongo_client.connect()

   mongo_database_log = mongo_client[EnvVariables.MONGODB_DATABASE_LOG]

   fluxo_husky_repository = FluxoHuskyRepository(db=mongo_database_log)
