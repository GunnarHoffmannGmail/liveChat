 import streamlit as st
import streamlit.components.v1 as components
import base64

# Embed custom HTML and JavaScript to capture audio from the microphone
audio_capture_html = """
    <html>
        <body>
            <h3>Click the button to start recording audio</h3>
            <button id="startBtn">Start Recording</button>
            <script>
                const startBtn = document.getElementById('startBtn');
                let mediaRecorder;
                let audioChunks = [];

                startBtn.onclick = () => {
                    if (navigator.mediaDevices) {
                        navigator.mediaDevices.getUserMedia({ audio: true })
                            .then(function(stream) {
                                mediaRecorder = new MediaRecorder(stream);
                                
                                mediaRecorder.ondataavailable = function(event) {
                                    audioChunks.push(event.data);
                                    // Once recording stops, send the audio to the server
                                    if (mediaRecorder.state === 'inactive') {
                                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                                        const reader = new FileReader();
                                        reader.onload = function() {
                                            const audioData = reader.result.split(',')[1];  // Base64 encoded
                                            window.parent.postMessage({ type: 'audio', data: audioData }, '*');
                                        };
                                        reader.readAsDataURL(audioBlob);
                                    }
                                };

                                mediaRecorder.start();
                                setTimeout(() => { 
                                    mediaRecorder.stop();
                                }, 5000); // Record for 5 seconds
                            });
                    }
                };
            </script>
        </body>
    </html>
"""

# Display the custom HTML component
components.html(audio_capture_html, height=300)
