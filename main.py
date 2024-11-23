import streamlit as st

# Set the title of the app
st.title("Welcome to My Streamlit App")

# Add a subtitle
st.subheader("A simple app to demonstrate Streamlit features")

# Add a greeting message
st.markdown("### Hello, World!")

# Create two columns
col1, col2 = st.columns(2)

# Add an input box for an integer in the first column
with col1:
    number = st.number_input("Enter an integer", min_value=0, max_value=100, value=0)

# Display the entered number in the second column
with col2:
    st.write(f"You entered: {number}")

# Add a footer
st.markdown("---")
st.markdown("**Thank you for using the app!**")
