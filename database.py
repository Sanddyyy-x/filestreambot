from pymongo import MongoClient
import os
import uuid

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["filestream"]
collection = db["files"]

def save_file(file_id, file_name):
    unique_id = str(uuid.uuid4())
    collection.insert_one({
        "unique_id": unique_id,
        "file_id": file_id,
        "file_name": file_name
    })
    return unique_id

def get_file(unique_id):
    return collection.find_one({"unique_id": unique_id})
