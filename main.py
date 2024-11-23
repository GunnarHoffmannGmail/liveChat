import streamlit as st
import openai
import speech_recognition as sr
import sounddevice as sd
import queue
import threading

# Set up OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Function to recognize speech in real-time
def recognize_speech_live():
    recognizer = sr.Recognizer()
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            st.write(status)
        q.put(bytes(indata))

    with sr.Microphone() as source:
        st.write("Listening in live chat mode...")
        audio_stream = sd.InputStream(samplerate=16000, channels=1, callback=callback)
        with audio_stream:
            while True:
                audio_data = q.get()
                try:
                    audio = sr.AudioData(audio_data, 16000, 2)
                    text = recognizer.recognize_google(audio)
                    if text:
                        st.write(f"Recognized: {text}")
                        yield text
                except sr.UnknownValueError:
                    st.write("Listening...")
                except sr.RequestError:
                    st.write("Sorry, my speech service is down.")
                    break

# Function to process input using OpenAI GPT-3
def process_input(text):
    response = openai.Completion.create(
        engine="davinci",
        prompt=text,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Streamlit app layout
st.title("Live Chat Mode with Speech Recognition")
st.subheader("This app listens to live speech and displays recognized text in real-time.")

if st.button("Start Live Chat Listening"):
    for recognized_text in recognize_speech_live():
        response = process_input(recognized_text)
        st.write(f"Response: {response}")
