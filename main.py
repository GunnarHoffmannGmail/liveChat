import streamlit as st
import speech_recognition as sr
import json
from google.cloud import speech

# Set up Google API credentials from Streamlit secrets
google_api_key_json = st.secrets["google_api_key_json"]

# Initialize the Google Cloud Speech client
client = speech.SpeechClient.from_service_account_info(json.loads(google_api_key_json))

# Streamlit app configuration
st.title("Live Speech-to-Text App")
st.text("Press the button and speak into your microphone to see the live transcription below!")

# Function to listen to audio and recognize text
def listen_and_transcribe():
    recognizer = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as source:
        st.text("Listening...")
        try:
            audio_data = recognizer.listen(source, timeout=10)  # Listen for 10 seconds max
            st.text("Transcribing...")
            audio_content = audio_data.get_wav_data()

            # Configure Google Speech-to-Text
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
            )

            request = speech.RecognizeRequest(
                config=config,
                audio=speech.RecognitionAudio(content=audio_content),
            )

            response = client.recognize(request=request)

            if response.results:
                for result in response.results:
                    transcript = result.alternatives[0].transcript
                    st.write(transcript)
            else:
                st.write("No speech detected.")

        except sr.WaitTimeoutError:
            st.error("Listening timed out, please try again.")
        except sr.RequestError:
            st.error("Could not request results, check your internet connection.")
        except sr.UnknownValueError:
            st.error("Could not understand the audio, please speak clearly.")

if st.button("Start Listening"):
    listen_and_transcribe()
