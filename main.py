from google.cloud import speech
import io

def transcribe_audio(audio_data):
    # Initialize the Speech client
    client = speech.SpeechClient()

    # Audio configuration
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Perform the transcription
    response = client.recognize(config=config, audio=audio)

    # Extract the transcription
    transcriptions = []
    for result in response.results:
        transcriptions.append(result.alternatives[0].transcript)
    
    return " ".join(transcriptions)
