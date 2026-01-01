import streamlit as st
import os
import json
import time
import google.generativeai as genai
import chromadb
from chromadb.config import Settings
from chromadb import Documents, EmbeddingFunction, Embeddings
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(page_title="FUTMinna Chatbot", page_icon="🤖")
st.title("🤖 FUTMinna Chatbot")

# Load Gemini API Key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Please set your GEMINI_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=api_key)

# Custom Embedding Function using Gemini
class GeminiEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.model = "models/text-embedding-004"  # Latest stable embedding model

    def __call__(self, input: Documents) -> Embeddings:
        # Detect if it's query or document mode based on context (Chroma handles this via collection settings)
        # But we use task_type dynamically if possible
        embeddings = []
        for text in input:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document" if len(input) > 1 else "retrieval_query"
            )
            embeddings.append(result["embedding"])
        return embeddings

# Initialize Chroma client with persistence
chroma_client = chromadb.PersistentClient(path="./chroma_data")

collection_name = "futminna_handbook"
embedding_function = GeminiEmbeddingFunction()

# Get or create collection
collection = chroma_client.get_or_create_collection(
    name=collection_name,
    embedding_function=embedding_function
)

# Load and embed handbook chunks (only once)
if "embedding_done" not in st.session_state:
    st.session_state.embedding_done = False

if not st.session_state.embedding_done:
    try:
        with open("chunked_text.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)

        if chunks:
            collection.add(
                documents=chunks,
                ids=[f"chunk_{i}" for i in range(len(chunks))]
            )
            st.session_state.embedding_done = True
            st.success("Student handbook loaded and embedded successfully!")
        else:
            st.warning("chunked_text.json is empty.")
    except FileNotFoundError:
        st.error("chunked_text.json not found. Please add the file to the project root.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading chunks: {e}")
        st.stop()

# Initialize chat history and model
if "messages" not in st.session_state:
    st.session_state.messages = []

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = genai.GenerativeModel("gemini-2.5-flash")  # Latest Flash model

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about FUTMinna policies, rules, or procedures..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving relevant information..."):
            # Retrieve top 5 relevant passages
            results = collection.query(
                query_texts=[prompt],
                n_results=5
            )
            relevant_passages = "\n\n".join(results["documents"][0]) if results["documents"] else ""

        # Prepare prompt
        system_prompt = f"""
You are FUTMinna Chatbot, a friendly and helpful assistant for students of Federal University of Technology Minna, Nigeria.
Answer questions accurately using only the provided context from the official student handbook.
Be detailed, clear, polite, and conversational. Use complete sentences.
If the user greets you (e.g., "hi", "hello"), greet back, introduce yourself briefly, and ask how you can help.
Otherwise, go straight to answering the question without introducing yourself.
Do not mention that you are using a passage or context.
Do not hallucinate or add information not present in the context.
If the context is irrelevant, say you don't have information on that topic from the handbook.

QUESTION: {prompt}
CONTEXT:
{relevant_passages}
"""

        # Generate response
        try:
            response = st.session_state.gemini_model.generate_content(
                system_prompt,
                stream=True
            )

            # Stream the response
            placeholder = st.empty()
            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error generating response: {e}")
            full_response = "Sorry, I encountered an issue. Please try again."

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_response})