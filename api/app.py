from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langserve import add_routes
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize FastAPI app
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server for essay and poem generation"
)

# Initialize Google Generative AI model
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7
)

# Define prompt templates
prompt1 = ChatPromptTemplate.from_template(
    "Write me an essay about {topic} with 100 words"
)
prompt2 = ChatPromptTemplate.from_template(
    "Write me a poem about {topic} for a 5 year old child with 100 words"
)

# Add routes for both endpoints
add_routes(
    app,
    prompt1 | llm,  # Changed from model to llm
    path="/essay"
)

add_routes(
    app,
    prompt2 | llm,
    path="/poem"
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)