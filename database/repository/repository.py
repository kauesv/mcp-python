from pymongo.database import Database


class Repository:
    """
    class utilitária de repository
    nunca será usada isolada, outras repository dependem dessa class
    """

    def __init__(self, db: Database, collection_name: str):
        self.db = db
        self.collection = db.get_collection(collection_name)