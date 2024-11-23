import streamlit as st
import openai
import speech_recognition as sr
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play
from pydub.generators import Sine
import tempfile

# Set up OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Function to recognize speech using pydub
def recognize_speech():
    recognizer = sr.Recognizer()
    duration = 5  # seconds
    fs = 44100  # Sample rate
    st.write("Listening...")

    # Generate a silent audio segment
    silent_segment = Sine(0).to_audio_segment(duration=duration * 1000)

    # Save the silent audio segment to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        silent_segment.export(temp_audio_file.name, format="wav")
        temp_audio_file_path = temp_audio_file.name

    with sr.AudioFile(temp_audio_file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        st.write(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.write("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        st.write("Sorry, my speech service is down.")
        return ""

# Function to process input using OpenAI GPT-3
def process_input(text):
    response = openai.Completion.create(
        engine="davinci",
        prompt=text,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    response_audio = AudioSegment.from_mp3("response.mp3")
    play(response_audio)

# Streamlit app layout
st.title("Welcome to My Streamlit App")
st.subheader("A simple app to demonstrate Streamlit features")
st.markdown("### Hello, World!")
st.markdown("---")

# Create two columns
col1, col2 = st.columns(2)

# Add an input box for an integer in the first column
with col1:
    st.markdown("#### Input Section")
    number = st.number_input("Enter an integer", min_value=0, max_value=100, value=0)

# Display the entered number in the second column
with col2:
    st.markdown("#### Output Section")
    st.write(f"You entered: {number}")

# Add an image
st.image("https://via.placeholder.com/800x200.png?text=Streamlit+App", use_column_width=True)

# Add a horizontal line
st.markdown("---")

# Voice assistant section
st.markdown("### Voice Assistant Chatbot")
st.write("Press the button and start speaking...")

if st.button("Start Listening"):
    user_input = recognize_speech()
    if user_input:
        response = process_input(user_input)
        st.write(f"Response: {response}")
        text_to_speech(response)

# Add a footer with a link
st.markdown("---")
st.markdown("**Thank you for using the app!**")
st.markdown("[Learn more about Streamlit](https://streamlit.io)")
