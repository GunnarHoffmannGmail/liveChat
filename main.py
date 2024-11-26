import streamlit as st
import sounddevice as sd
import numpy as np
import queue
import threading
from google.cloud import speech
import os

# Set up Google API credentials from Streamlit secrets
google_api_key_json = st.secrets["google_api_key_json"]

# Initialize the Google Cloud Speech client
import json
client = speech.SpeechClient.from_service_account_info(json.loads(google_api_key_json))

# Streamlit app configuration
st.title("Live Speech-to-Text App")
st.text("Speak into your microphone and see the live transcription below!")

# Audio recording configuration
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# Queue to communicate between the audio callback and main thread
audio_queue = queue.Queue()

# Function to capture audio from microphone
def microphone_stream():
    def callback(indata, frames, time, status):
        if status:
            st.error(f"Error: {status}")
        audio_queue.put(indata.copy())

    stream = sd.InputStream(
        samplerate=RATE,
        channels=1,
        callback=callback,
        blocksize=CHUNK
    )
    return stream

# Function to listen to audio and recognize text
def listen_print_loop():
    stream = microphone_stream()
    with stream:
        stream.start()
        audio_generator = stream_generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code="en-US",
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )

        responses = client.streaming_recognize(streaming_config, requests)
        process_responses(responses)

# Generator to yield audio chunks
def stream_generator():
    while True:
        chunk = audio_queue.get()
        if chunk is None:
            return
        yield chunk.tobytes()

# Function to process responses from Google Speech-to-Text
def process_responses(responses):
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        st.write(transcript)

# Start listening in a separate thread
def start_listening():
    listen_thread = threading.Thread(target=listen_print_loop)
    listen_thread.start()

if st.button("Start Listening"):
    start_listening()
