import pymongo
import gridfs
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

MONGO_URI = config["MONGO_URI"]
DATABASE_NAME = config["DATABASE_NAME"]
# Connect to MongoDB Atlas
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Create a GridFS instance
fs = gridfs.GridFS(db)

# Upload audio file to MongoDB
def upload_audio_to_mongo(file_path, file_name):
    try:
        # Check if a file with the same name exists
        existing_file = fs.find_one({"filename": file_name})
        if existing_file:
            # Delete the existing file
            fs.delete(existing_file._id)
            print(f"Deleted old file with name: {file_name}")

        # Upload the new file
        with open(file_path, 'rb') as file_data:
            file_id = fs.put(file_data, filename=file_name)
            print(f"File uploaded successfully! File ID: {file_id}")
    except Exception as e:
        print(f"Error occurred: {e}")


