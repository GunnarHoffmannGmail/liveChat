import streamlit as st
import openai
import speech_recognition as sr
from gtts import gTTS
import os

# Set up OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
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
    os.system("mpg321 response.mp3")

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
