import streamlit as st

st.write("Hello, World!")

# Add an input box for an integer
number = st.number_input("Enter an integer", min_value=0, max_value=100, value=0)

# Display the entered number
st.write(f"You entered: {number}")
