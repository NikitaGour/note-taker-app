from pymongo import MongoClient
import os
conn=MongoClient(os.getenv("MONGO_URI"))
