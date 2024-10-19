from pymongo import MongoClient
from flask import Flask, request, jsonify
import os, json

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

if not SECRET_KEY or not DATABASE_URL:
    raise ValueError("SECRET_KEY or DATABASE_URL are not defined in .env")

else:
    DATABASE_URL = DATABASE_URL.replace('<db_password>', SECRET_KEY)
    client = MongoClient(DATABASE_URL)
    db = client['database']
    collection = db['users']

try:
    dbtest = client.test
    print("Connected successfully!")

except Exception as e:
    print('Error while connecting to MongoDB', e)

app = Flask(__name__)

@app.route('/upload-json', methods=['POST'])

def upload_json():
    if 'file' not in request.files:
        return jsonify({"error": "No file was uploaded"}), 400
    
    file = request.files['file']

    if not file.filename.endswith('.json'):
        return jsonify({"error": "Invalid file type. PLease upload a .json file"}), 400
    
    try:
        data = file.read()

        data_dict = json.loads(data)

        collection.insert_many(data_dict)
    
        return jsonify({"message": "JSON file was uploaded successfully"}), 201
    
    except Exception as e:
        return jsonify({"error": "An error occurred while uploading the json file: " + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)