import requests
import streamlit as st

# Function to invoke the essay API
def hello_google(input_text):
    try:
        response = requests.post("http://localhost:8000/essay/invoke",
                                 json={'input': {'topic': input_text}})
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json().get('output', {}).get('content', "No content returned")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Function to invoke the poem API
def hello_llama(input_text):
    try:
        response = requests.post("http://localhost:8000/poem/invoke",
                                 json={'input': {'topic': input_text}})
        response.raise_for_status()
        return response.json().get('output', {}).get('content', "No content returned")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Streamlit UI
st.title('DEMO LangChain')

# Input fields
input_text = st.text_input("Enter topic for Google (Essay):")
input_text2 = st.text_input("Enter topic for Llama (Poem):")

# Display responses
if input_text:
    st.write("Essay Response:")
    st.write(hello_google(input_text))

if input_text2:
    st.write("Poem Response:")
    st.write(hello_llama(input_text2))
