from dotenv import load_dotenv
import os
import pymongo
import flask
import pandas as pd

load_dotenv()

secretKey = os.getenv("SECRET_KEY")
databaseUrl = os.getenv("DATABASE_URL")

if not secretKey or not databaseUrl:
    raise ValueError("SECRET_KEY ou DATABASE_URL não estão definidos no .env")

else:
    client = databaseUrl.replace('<db_password>', secretKey)
    db = client['database']
    collection = db['users']


