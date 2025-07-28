from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
mongo_uri= os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["vendo"]
user_collection = db["users"]
print("MongoDB connection established successfully!")

users = list(user_collection.find({}, {"_id": 0}))



def get_vendor_data(vendor_username: str):
    try:
        vendor_data = user_collection.find_one({"username": vendor_username})
        return vendor_data
    except Exception as e:
        print(f"Error fetching vendor data: {e}")
        return None

def get_supplier_data():
    suppliers = [u for u in users if u["type"] == "supplier"]
    return suppliers
