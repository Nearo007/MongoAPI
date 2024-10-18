from dotenv import load_dotenv
import os
from pymongo import MongoClient
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

load_dotenv()

secretKey = os.getenv("SECRET_KEY")
databaseUrl = os.getenv("DATABASE_URL")

if not secretKey or not databaseUrl:
    raise ValueError("SECRET_KEY or DATABASE_URL are not defined in .env")

else:
    databaseUrl = databaseUrl.replace('<db_password>', secretKey)
    client = MongoClient(databaseUrl)
    db = client['database']
    collection = db['users']

try:
    db = client.test
    print("Connected successfully!")

except Exception as e:
    print('Error while connecting to MongoDB', e)

@app.route('/upload-excel', methods=['POST'])

def upload_excel():
    if 'file' not in request.files:
        return jsonify({"error": "No file was uploaded"}), 400
    
    file = request.files['file']

    if not file.filename.endswith('.xlsx'):
        return jsonify({"error": "Invalid file. Please upload an excel file."}), 400
    
    try:
        df = pd.read_excel(file)

        data_dict = df.to_dict(orient='records')
        collection.insert_many(data_dict)

        return jsonify({"message": "Excel file was uploaded successfully"}), 201
    
    except Exception as e:
        return jsonify({"error": "An error occurred while uploading the excel file: " + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)