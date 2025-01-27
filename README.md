# SEC-Filing-Agentic-AI

This repository contains a Python-based application for SEC Filing summary and query that integrates speech recognition and text-to-speech functionalities with a Reflex-based web UI. It uses the Langflow API for advanced NLP processing and integrates Astra DB, Groq model, and chat memory for enhanced interaction.

## Features

- **Speech-to-Text**: Converts user speech to text using Google Speech Recognition.
- **Text-to-Speech**: Converts text responses to speech and saves them as audio files.
- **API Integration**: Uses Langflow API with Astra DB and Groq model for advanced NLP processing.
- **Real-time Interaction**: Continuously listens for user input until the chat is stopped.
- **Chat Memory**: Remembers previous interactions for more contextually aware responses.
- **Audio File Management**: Uploads audio responses to MongoDB for storage.
- **Reflex UI**: Simple and intuitive web interface for user interaction.

## Technologies Used

- **Python Libraries**:
  - `speech_recognition`: For speech-to-text conversion.
  - `pyttsx3`: For text-to-speech conversion.
  - `requests`: For API requests.
  - `asyncio`: For asynchronous programming.
  - `wave` and `contextlib`: For audio file management.
  - `os`: For file operations.
  
- **Web Framework**: Reflex (for creating the web interface).
  
- **Database**: Astra DB (for advanced data management and storage).
  
- **Model**: Groq (used for AI processing in the flow).

- **Database for Audio**: MongoDB (for storing audio responses).

## Langflow API Integration

The Langflow API integrates several critical features for the project:

- **Astra DB**: Used for handling and managing structured data within the application.
- **Groq Model**: Powers the NLP processing for better chat response generation.
- **Chat Memory**: Retains conversation history to provide more context-aware replies.
- **Tweak Options**: Provides customization for handling specific interactions in the flow.

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

5. **Run the `AudioServer.py` script** to handle audio file management before starting the Reflex app:

   ```bash
   python AudioServer.py
   ```

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

## File Structure

- **`audioServer.py`**: Handles audio file streaming and retrieval from MongoDB.
- **`AIAgent.py`**: Main application file containing all logic for the Reflex app.
- **`upload.py`**: Contains logic for uploading audio files to MongoDB.
- **Audio Files**: Temporarily saved in the root directory (deleted after processing).

## Future Improvements

- Add support for multiple languages in speech recognition and text-to-speech.
- Enhance the UI for a more user-friendly experience.
- Implement real-time transcription display.
- Add error handling for better API response debugging.
