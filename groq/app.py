import streamlit as st
import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
import time
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.environ['GROQ_API_KEY']

if "vector" not in st.session_state:
    st.session_state.embeddings = OllamaEmbeddings(model="llama3")
    st.session_state.loader = WebBaseLoader("https://uselessai.in/introduction-to-machine-learning-e272cf75b5b0")
    st.session_state.docs = st.session_state.loader.load()

    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
    st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

st.title("Chat GROQ demo")
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="Deepseek-R1-Distill-Llama-70b"
)

# Create a proper ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", """
    Answer the question based on the provided context only.
    Please provide the most accurate response based on the question.
    
    Context: {context}
    """),
    ("user", "{input}")
])

# Create the document chain
document_chain = create_stuff_documents_chain(llm, prompt)

# Create retriever and retrieval chain
retriever = st.session_state.vectors.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Streamlit UI
prompt_input = st.text_input("Input your prompt here")

if prompt_input:
    start = time.time()
    response = retrieval_chain.invoke({"input": prompt_input})
    st.write(response['answer'])
    end = time.time()
    st.write(f"Response time: {end - start:.2f} seconds")