from flask import Flask, send_file, Response
from io import BytesIO
import pymongo
import gridfs
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

MONGO_URI = config["MONGO_URI"]
DATABASE_NAME = config["DATABASE_NAME"]

client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
fs = gridfs.GridFS(db)


app = Flask(__name__)


@app.route('/audio/<filename>', methods=['GET'])
def get_audio(filename):
    """
    Serve the audio file stored in MongoDB GridFS.

    :param filename: Name of the audio file in MongoDB
    :return: Audio file as a response
    """
    try:
        # Retrieve the file from GridFS
        file_data = fs.find_one({"filename": filename})
        if not file_data:
            return Response("File not found", status=404)

        # Read the file content
        audio_stream = BytesIO(file_data.read())
        return send_file(audio_stream, mimetype='audio/mpeg', as_attachment=False, download_name=filename)

    except Exception as e:
        return Response(f"Error occurred: {str(e)}", status=500)

if __name__ == '__main__':
    app.run(debug=True)