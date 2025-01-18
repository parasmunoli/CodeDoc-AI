import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

url = os.environ.get('MONGODB_URL')

client = pymongo.MongoClient(url)

db = client['CodeDocAI']