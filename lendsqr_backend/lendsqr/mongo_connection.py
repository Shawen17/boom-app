# mongo_connection.py
import pymongo
from decouple import config

class MongoConnection:
    _instance = None

    @staticmethod
    def get_instance():
        if MongoConnection._instance is None:
            MongoConnection()
        return MongoConnection._instance

    def __init__(self):
        if MongoConnection._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self._instance = self
            self.client = None
            self.connect()

    def connect(self):
        db_user = config("DB_USER")
        db_password = config("PASSWORD")
        db_cluster = config("CLUSTERNAME")
        self.client = pymongo.MongoClient(f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority")

    def get_db(self, db_name):
        return self.client[db_name]

    def shutdown(self):
        return self.client.close()


# client= MongoConnection()
# db= client.get_db("user_details")
# print(db['users'].count_documents({}))

# client.shutdown()
# Use mongo_connection.get_db('your_db_name') to get the database instance and perform operations
