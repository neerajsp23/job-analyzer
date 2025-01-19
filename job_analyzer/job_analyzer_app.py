from fastapi import FastAPI, UploadFile, HTTPException, Form
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from job_analyzer.analyzer import stream_response, process_audio

from ollama import chat
from fastapi import FastAPI, UploadFile, File, HTTPException
import speech_recognition as sr
from io import BytesIO

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


app = FastAPI(title="Task Summarizer API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.post("/")
async def process_input(
    input_string: Optional[str] = Form(None),  # Accept text input from form-data
    audio_file: Optional[UploadFile] = None   # Accept audio file
):
    global Flag
    # If both input_string and audio_file are None, return an error
    if not input_string and not audio_file:
        raise HTTPException(status_code=400, detail="Either text or audio must be provided.")

    # Process audio input if provided
    if not input_string and audio_file:
        input_string = await process_audio(audio_file)

    if input_string:
        messages = [
            {
                "role": "user",
                "content": PROMPT.format(input_string),
            }
        ]
        model = "tinyllama" if Flag else "orca-mini"
        Flag = not Flag
        return StreamingResponse(stream_response(model, messages), media_type="text/plain")
    
    raise HTTPException(status_code=400, detail="Unable to process the input.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
