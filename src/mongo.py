from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['scraper']

sony_collection = db['sony']

