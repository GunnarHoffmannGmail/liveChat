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

            document.getElementById('startButton').addEventListener('click', async () => {
                stopFlag = false;
                document.getElementById('startButton').disabled = true;
                document.getElementById('stopButton').disabled = false;
                audioChunks = [];

                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    console.log("Microphone access granted.");
                    mediaRecorder = new MediaRecorder(stream);

                    mediaRecorder.addEventListener('dataavailable', event => {
                        audioChunks.push(event.data);
                    });

                    mediaRecorder.addEventListener('stop', async () => {
                        if (stopFlag) {
                            return;
                        }

                        console.log("MediaRecorder stopped, processing audio...");
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                        const reader = new FileReader();
                        reader.readAsDataURL(audioBlob);
                        reader.onloadend = async () => {
                            const base64AudioMessage = reader.result.split(',')[1];
                            
                            const apiKey = "{api_key}";
                            const requestPayload = {{
                                audio: {{
                                    content: base64AudioMessage
                                }},
                                config: {{
                                    encoding: "LINEAR16",
                                    sampleRateHertz: 16000,
                                    languageCode: "en-US"
                                }}
                            }};

                            try {
                                console.log("Sending audio data to Google Speech-to-Text API...");
                                const response = await fetch(
                                    `https://speech.googleapis.com/v1/speech:recognize?key=${{apiKey}}`,
                                    {{
                                        method: "POST",
                                        headers: {{
                                            "Content-Type": "application/json"
                                        }},
                                        body: JSON.stringify(requestPayload)
                                    }}
                                );
                                const responseData = await response.json();

                                if (responseData.results) {{
                                    const transcript = responseData.results.map(result => result.alternatives[0].transcript).join("\\n");
                                    document.getElementById('transcript').value += transcript + "\\n";
                                }} else {{
                                    console.log("No transcription result returned.");
                                }}
                            }} catch (error) {{
               
