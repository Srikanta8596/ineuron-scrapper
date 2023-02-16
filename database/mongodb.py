import pymongo
import certifi
ca=certifi.where()
from database.configuration import MONGO_DB_CONNECTION_STRING, MONGO_DATA_BASE_NAME, MONGO_COLLECTION_NAME
class MongodbOperation:
    def __init__(self):
        self.db_name = MONGO_DATA_BASE_NAME
        self.client=pymongo.MongoClient(MONGO_DB_CONNECTION_STRING)
    
    def insert_many(self,records: list):
        self.client[self.db_name][MONGO_COLLECTION_NAME].insert_many(records)

    def insert(self,record: dict):
        self.client[self.db_name][MONGO_COLLECTION_NAME].insert_one(record)