Here's the updated README with the necessary instructions to run `audioServer.py` before the Reflex app:

---

# SEC-Filing-Agentic-AI

This repository contains a Python-based application that integrates speech recognition and text-to-speech functionalities with a Reflex-based web UI. It uses an external API to process user inputs and provides audio responses.

## Features

- **Speech-to-Text**: Converts user speech to text using Google Speech Recognition.
- **Text-to-Speech**: Converts text responses to speech and saves them as audio files.
- **API Integration**: Uses Langflow API for advanced NLP processing.
- **Real-time Interaction**: Continuously listens for user input until the chat is stopped.
- **Audio File Management**: Uploads audio responses to MongoDB for storage.
- **Reflex UI**: Simple and intuitive web interface for user interaction.

---

## Technologies Used

- **Python Libraries**:

  - `speech_recognition`: For speech-to-text conversion.
  - `pyttsx3`: For text-to-speech conversion.
  - `requests`: For API requests.
  - `asyncio`: For asynchronous programming.
  - `wave` and `contextlib`: For audio file management.
  - `os`: For file operations.

- **Web Framework**: Reflex (for creating the web interface).

- **Database**: MongoDB (for storing audio responses).

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   ```

2. Navigate to the project directory:

   ```bash
   cd your-repo-name
   ```

3. Install required Python libraries:

   ```bash
   pip install reflex speechrecognition pyttsx3 requests pymongo
   ```

4. Add your Langflow API credentials to the constants section in the Python file:

   ```python
   BASE_API_URL = "https://api.langflow.astra.datastax.com"
   LANGFLOW_ID = "your-langflow-id"
   FLOW_ID = "your-flow-id"
   APPLICATION_TOKEN = "your-application-token"
   ```

5. **Run the `audioServer.py` script** to handle audio file management before starting the Reflex app:

   ```bash
   python audioServer.py
   ```

---

## Usage

1. Run the Reflex application:

   ```bash
   reflex run
   ```

2. Open the application in your browser:

   - Navigate to `http://127.0.0.1:5000`.

3. Use the interface to start/stop listening.

   - **Start Listening**: Click the button to begin speech recognition.
   - **Stop Listening**: Click the button or say "Stop the chat" to end the session.

4. View and listen to the generated responses directly in the UI.

---

## File Structure

- **`audioServer.py`**: Handles audio file streaming and retrieval from MongoDB.
- **`app.py`**: Main application file containing all logic for the Reflex app.
- **`upload.py`**: Contains logic for uploading audio files to MongoDB.
- **Audio Files**: Temporarily saved in the root directory (deleted after processing).

---

## Future Improvements

- Add support for multiple languages in speech recognition and text-to-speech.
- Enhance the UI for a more user-friendly experience.
- Implement real-time transcription display.
- Add error handling for better API response debugging.

---