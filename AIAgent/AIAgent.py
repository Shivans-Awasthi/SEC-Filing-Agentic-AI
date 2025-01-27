import reflex as rx
from typing import Optional
import requests
import speech_recognition as sr
import pyttsx3
from upload import upload_audio_to_mongo
import time
import wave
import contextlib
import os
import asyncio
import random
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)


# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = config["LANGFLOW_ID"]
FLOW_ID = config["FLOW_ID"]
APPLICATION_TOKEN = config["APPLICATION_TOKEN"]

# Path to save audio files
AUDIO_FILE_PATH = "response_audio.mp3"


sessionID = random.randrange(1,1000)

TWEAKS = {
  "TextInput-mEP51": {
    "input_value": f"{sessionID}"
  }
}


def run_flow(message: str, endpoint: str, output_type: str = "chat", input_type: str = "chat", tweaks: Optional[dict] = None, application_token: Optional[str] = None) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def get_audio_duration(file_path: str) -> float:
    """Get the duration of an audio file in seconds."""
    with contextlib.closing(wave.open(file_path, 'r')) as audio_file:
        frames = audio_file.getnframes()
        rate = audio_file.getframerate()
        return frames / float(rate)




class State(rx.State):
    messages: Optional[str] = None
    audio_url: Optional[str] = None
    is_listening: bool = False
    status: Optional[str] = "Idle"
    running: bool = False

    def add_message(self, message: str):
        self.set(messages=message)
        
    def set_running(self, value: bool):
        self.set(running=value)

    def add_audio_url(self, url: str):
        self.set(audio_url=url)

    def set_is_listening(self, value: bool):
        self.set(is_listening=value)

    def add_status(self, status: str):
        self.set(status=status)

    async def text_to_speech(self, text: str):
        def _synthesize_text():
            engine = pyttsx3.init()
            engine.save_to_file(text, AUDIO_FILE_PATH)
            engine.runAndWait()

        await asyncio.to_thread(_synthesize_text)
        print("Added new audio")
        
    async def stopApp(self):
            self.set_running(False)
            self.set_is_listening(False)
            # await self.text_to_speech("Your Welcome any time")
            # await asyncio.to_thread(upload_audio_to_mongo, AUDIO_FILE_PATH, 'audio.mp3')
            # self.add_audio_url(f"http://127.0.0.1:5000/audio/audio.mp3?t={int(time.time())}")          
            # if os.path.exists(AUDIO_FILE_PATH):
            #     os.remove(AUDIO_FILE_PATH)
        

    async def speech_to_text(self):
        recognizer = sr.Recognizer()
        
        def _record_audio():
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.7)
                audio = recognizer.listen(source)
                return recognizer.recognize_google(audio)

        try:
            self.add_status("Listening...")
            return await asyncio.to_thread(_record_audio)
        except sr.UnknownValueError:
            return "NULL"
        except sr.RequestError as e:
            return f"Request error: {e}"

    async def process_message(self, user_message: str):
                            
        
        if user_message.lower() == "stop the chat" :
            await self.stopApp()

        
        if user_message.lower() == "stop" :
            await self.stopApp()
            
          
                                          
        else:       
            try:
                response = run_flow(
                message=user_message,
                endpoint=FLOW_ID,
                output_type="chat",
                input_type="chat",
                application_token=APPLICATION_TOKEN
                )

                text = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
                
                self.add_status("Done")
                self.add_message(f"System: {text}")
            
                await self.text_to_speech(text)
                await asyncio.to_thread(upload_audio_to_mongo, AUDIO_FILE_PATH, 'audio.mp3')

                timestamp = int(time.time())
                self.add_audio_url(f"http://127.0.0.1:5000/audio/audio.mp3?t={timestamp}")

            except KeyError:
                self.add_message("Error in response format. Check the API response.")
                await self.text_to_speech("Sorry, there was an error in processing your request.")
                self.add_audio_url(f"http://127.0.0.1:5000/audio/audio.mp3?t={int(time.time())}")

            except Exception as e:
                self.add_message(f"An error occurred: {e}")

            finally:
                if os.path.exists(AUDIO_FILE_PATH):
                    os.remove(AUDIO_FILE_PATH)

            self.set_is_listening(False)
            

        


    async def start_listening_process(self):
        self.add_status("Listening...")
    
        user_message = await self.speech_to_text()

        await self.process_message(user_message)
        if self.running: 
            self.add_status("Speaking...")
        else:
            self.add_status("App Exited..")

    async def toggle_listening(self):
        self.is_listening = not self.is_listening
        if not self.running :
            self.set_running(True)


        while self.is_listening and self.running:
            self.add_status("Listening...say 'Stop the chat' to stop")
            yield
            
            if not self.running:
                break
            await self.start_listening_process()

      
            
                        
# Reflex UI
def index() :
    return rx.fragment(
        rx.center(
            rx.vstack(
                rx.button(
                    rx.cond(
                        State.is_listening,
                        rx.text("Stop Listening"),
                        rx.text("Start Listening"),
                    ),
                    on_click=State.toggle_listening,   
                    style={
                        "marginTop": "200px",
                        "padding": "10px",
                    }
                ),
                rx.cond(
                    State.status,
                    rx.text(State.status, style={
                        "marginTop": "20px",
                        "marginLeft": "10px",
                    }),  
                    rx.text("Idle", style={
                        "marginTop": "20px",
                        "marginLeft": "10px",
                    })  
                ),
                spacing="2",
            ),
        ),
        rx.center(
            rx.text(State.messages, style={
                    "padding": "5px",
                    "maxWidth": "60%",
                    "maxHeight": "300px",
                    "marginTop": "50px"
                }),
        ),

                rx.cond(
                    State.is_listening,
                    rx.audio(
                        controls=False,
                        url=State.audio_url,
                        playing=False,
                        width="400px",
                        height="32px",
                    ),
                    rx.audio(
                        controls=False,
                        url=State.audio_url,
                        playing=True,
                        width="400px",
                        height="32px",
                    ),
                    ),
                    
                ),
                

app = rx.App()
app.add_page(index)








