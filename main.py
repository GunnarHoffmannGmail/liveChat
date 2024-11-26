import streamlit as st
import streamlit.components.v1 as components

# Streamlit app configuration
st.title("Live Speech-to-Text App with Microphone")

# Extract Google API key from secrets
api_key = st.secrets["mykey"]["api_key"]

# Embed the HTML code using Streamlit's components.html function
components.html(
    f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Live Speech-to-Text with Google API</title>
    </head>
    <body>
        <h1>Live Speech-to-Text App with Microphone</h1>
        <p>Press 'Start' to begin capturing your speech!</p>
        
        <button id="startButton">Start Listening</button>
        <button id="stopButton" disabled>Stop Listening</button>
        <textarea id="transcript" rows="10" cols="100"></textarea>

        <script>
            let mediaRecorder;
            let audioChunks = [];
            let stopFlag = false;

            document.getElementById('startButton').addEventListener('click', async ()
