from fastapi import FastAPI, UploadFile, File, HTTPException , Form
from pydantic import BaseModel
from typing import Optional, List, Union, Dict
from enum import Enum
import random
import json
import speech_recognition as sr
from io import BytesIO
import ollama
from fastapi.responses import StreamingResponse
from job_analyzer.analyzer import process_tasks,process_audio
from fastapi.middleware.cors import CORSMiddleware

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
    # If both input_string and audio_file are None, return an error
    if not input_string and not audio_file:
        raise HTTPException(status_code=400, detail="Either text or audio must be provided.")
    # Process text input if provided
    if audio_file:
        input_string = await process_audio(audio_file)

    if input_string:
        return process_tasks(input_string)
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)