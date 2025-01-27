# Importing necessary libraries
import pymongo  # MongoDB client library
import gridfs   # MongoDB GridFS library for file storage
import json     # For loading the configuration file

# Open the 'config.json' file to load the MongoDB URI and database name
with open("config.json", "r") as config_file:
    config = json.load(config_file)  # Parse the JSON data into a dictionary

# Extract MongoDB connection parameters from the config file
MONGO_URI = config["MONGO_URI"]
DATABASE_NAME = config["DATABASE_NAME"]

# Connect to MongoDB Atlas using the provided URI
client = pymongo.MongoClient(MONGO_URI)

# Access the specified database
db = client[DATABASE_NAME]

# Create a GridFS instance to interact with file storage
fs = gridfs.GridFS(db)

# Function to upload an audio file to MongoDB using GridFS
def upload_audio_to_mongo(file_path, file_name):
    try:
        # Check if a file with the same name already exists in the GridFS collection
        existing_file = fs.find_one({"filename": file_name})
        
        if existing_file:
            # If a file exists, delete the old file from GridFS
            fs.delete(existing_file._id)
            print(f"Deleted old file with name: {file_name}")

        # Open the audio file in binary read mode and upload it to GridFS
        with open(file_path, 'rb') as file_data:
            file_id = fs.put(file_data, filename=file_name)  # Upload and store the file
            print(f"File uploaded successfully! File ID: {file_id}")
    except Exception as e:
        # Catch any exceptions and print an error message
        print(f"Error occurred: {e}")
