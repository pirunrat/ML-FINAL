from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, MONGODB_URI, MONGODB_NAME, collection_name):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_NAME]
        self.collection_name = collection_name

        if(self.client):
            print("Connected")
        else:
            print("Not Connected")

    def get_collection(self):
        return self.db[self.collection_name]

    def insert_one(self, data):
        collection = self.get_collection()
        return collection.insert_one(data).inserted_id

    def find_one(self, query):
        collection = self.get_collection()
        return collection.find_one(query)

    def find(self, query):
        collection = self.get_collection()
        return collection.find(query)

    def update_one(self, query, new_values):
        collection = self.get_collection()
        return collection.update_one(query, new_values)
    
    def update_many(self, query, new_values):
        collection = self.get_collection()
        return collection.update_many(query, new_values)

    def delete_one(self, query):
        collection = self.get_collection()
        return collection.delete_one(query)

    def close(self):
        self.client.close()
