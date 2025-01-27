from flask import Flask, send_file, Response
from io import BytesIO
import pymongo
import gridfs
import json

# Load the MongoDB configuration from the config.json file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# MongoDB URI and database name from the configuration
MONGO_URI = config["MONGO_URI"]
DATABASE_NAME = config["DATABASE_NAME"]

# Create a connection to MongoDB client
client = pymongo.MongoClient(MONGO_URI)

# Select the database
db = client[DATABASE_NAME]

# Initialize GridFS for handling large files in MongoDB
fs = gridfs.GridFS(db)

# Initialize the Flask application
app = Flask(__name__)

@app.route('/audio/<filename>', methods=['GET'])
def get_audio(filename):
    """
    Serve the audio file stored in MongoDB GridFS.
    
    This route retrieves the audio file based on the filename provided in the URL
    and sends it as a response to the client.

    :param filename: Name of the audio file stored in MongoDB
    :return: Audio file as a response or an error message
    """
    try:
        # Retrieve the file from GridFS using the filename
        file_data = fs.find_one({"filename": filename})
        
        # If the file is not found in the database, return a 404 error
        if not file_data:
            return Response("File not found", status=404)

        # Read the file content from GridFS and prepare it for sending
        audio_stream = BytesIO(file_data.read())
        
        # Send the file as an HTTP response with the appropriate MIME type (audio/mpeg)
        # and without forcing download (as_attachment=False)
        return send_file(audio_stream, mimetype='audio/mpeg', as_attachment=False, download_name=filename)

    except Exception as e:
        # If any error occurs, return a 500 error with the exception message
        return Response(f"Error occurred: {str(e)}", status=500)

# Run the Flask application in debug mode when executed directly
if __name__ == '__main__':
    app.run(debug=True)
