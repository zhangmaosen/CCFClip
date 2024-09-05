from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import gradio as gr
from datetime import datetime

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://127.0.0.1:7860",
    "http://localhost:9999",
    "http://localhost:7860",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path('./stream')
app.mount("/stream", StaticFiles(directory=static_dir), name="stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)