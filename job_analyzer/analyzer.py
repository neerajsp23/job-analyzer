from ollama import chat
from fastapi import FastAPI, UploadFile, File, HTTPException
import speech_recognition as sr
from io import BytesIO
from ollama import generate
# Prompt template to handle task extraction and status
PROMPT = '''
You are a helpful assistant. I will provide a description of tasks I am working on or plan to work on, and you should convert it into a JSON-like format strictly.
Each task will have a name and a status based on the description:
- Tasks mentioned as completed will have status "Done".
- Tasks described as currently being worked on will have status "In progress".
- Tasks mentioned as planned or future tasks will have status "Todo".

Example:
Input: "I have completed the floor work today, Right now working on tiles, and tomorrow I have to work on plumbing."
Output:
[
  {{ "task": "Floor Work", "status": "Done" }},
  {{ "task": "Tile Work", "status": "In progress" }},
  {{ "task": "Plumbing", "status": "Todo" }}
]

Note: The status should strictlybe one of the terms "Done", "In progress" or "Todo".
Also the output should be in the same format as that of the example

Now, provide the JSON-like output for the following input:
Input: "{0}"
Output:
'''

Flag=True

async def process_audio(audio_file: UploadFile) -> str:
    """Convert audio to text using speech recognition."""
    recognizer = sr.Recognizer()
    
    audio_bytes = await audio_file.read()
    audio_file_obj = BytesIO(audio_bytes)
    
    with sr.AudioFile(audio_file_obj) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing audio: {str(e)}")

# Streaming function
def stream_response(model, messages):
    # Extract the content string from the messages list
    prompt = messages[0]["content"]  # Get the "content" field of the first message
    for part in generate(model, prompt, stream=True):  # Pass the prompt as a string
        yield part["response"]
