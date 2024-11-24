import streamlit as st
from streamlit_mic_recorder import mic_recorder, speech_to_text

def callback(recognized_text, *args, **kwargs):
    st.session_state.text_received.append(recognized_text)

state = st.session_state

if 'text_received' not in state:
    state.text_received = []

c1, c2 = st.columns(2)
with c1:
    st.write("Convert speech to text:")
with c2:
    text = speech_to_text(language='en', use_container_width=True, just_once=False, key='STT', callback=lambda recognized_text: callback(recognized_text))

for text in state.text_received:
    st.text(text)

st.write("Record your voice, and play the recorded audio:")
audio = mic_recorder(start_prompt="⏺️", stop_prompt="⏹️", key='recorder')

if audio:
    st.audio(audio['bytes'])





