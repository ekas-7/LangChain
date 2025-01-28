# Import necessary libraries
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st 
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("Google API key not found. Please set it in the .env file.")
    st.stop()

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7
)

# Define the prompt template
prompt_template = ChatPromptTemplate.from_template(
    "You are a helpful assistant. Respond concisely and informatively to the user's query: {user_input}"
)

# Define the output parser
output_parser = StrOutputParser()

# Streamlit app interface
st.title("Chatbot with LangChain and Streamlit")
st.write("Ask any question and get a response!")

# User input
user_input = st.text_input("Enter your question here:")

# Generate response
# Generate response
if user_input:
    with st.spinner("Generating response..."):
        try:
            # Format the prompt with user input
            prompt = prompt_template.format(user_input=user_input)
            
            # Get the response from the model
            response = llm.invoke(prompt)  # Updated method
            
            # Parse the response
            parsed_response = output_parser.parse(response)
            
            # Display the response
            st.success(parsed_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
 