import streamlit as st
import time
import json
import google.generativeai as genai
import chromadb
from google.api_core import retry
from chromadb.config import Settings
from chromadb import Documents, EmbeddingFunction, Embeddings
#from IPython.display import Markdown
st.title("Futminna Chatbot")

genai.configure(api_key="AIzaSyBOe9KC0fATBuNlRNOHNLCZkdHeDooExec")
    
class GeminiEmbeddingFunction(EmbeddingFunction):
    # Specify whether to generate embeddings for documents, or queries
    document_mode = True

    def __call__(self, input: Documents) -> Embeddings:
        if self.document_mode:
            embedding_task = "retrieval_document"
        else:
            embedding_task = "retrieval_query"

        retry_policy = {"retry": retry.Retry(predicate=retry.if_transient_error)}

        response = genai.embed_content(
            model="models/text-embedding-004",
            content=input,
            task_type=embedding_task,
            request_options=retry_policy,
        )
        return response["embedding"]


chroma_client = chromadb.Client(Settings(persist_directory="./chroma_data"))

# Create or retrieve a collection
collection_name = "pdf_collection"

embed_fn = GeminiEmbeddingFunction()
if "collection" not in st.session_state:
        st.session_state.collection = chroma_client.get_or_create_collection(
            name=collection_name, embedding_function=embed_fn
        )
    
if "embedding_done" not in st.session_state:
    st.session_state.embedding_done = False

if not st.session_state.embedding_done:
    with open('chunked_text.json', 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    # Add chunked text to ChromaDB
    st.session_state.collection.add(
        documents=chunks,
        ids=[f"id_{i}" for i in range(len(chunks))],
    )
    st.session_state.embedding_done = True
else:
    pass


def prepare_prompt(query, passage, history):

    # This prompt is where you can specify any guidance on tone, or what topics the model should stick to, or avoid.
    prompt = f"""Your name is Futminna Chatbot. You are a helpful chatbot for Federal University of Technology Minna, Niger State, Nigeria a Technology University in Nigeria.
    You will provide students contextual and accurate answer to prompt provided. Clear students confusion based on their handbook., necessary passage related to the prompt extracted from the student handbook is included below.
    be detailed in your response giving as much word count as possible.
    don't make reference to the provided in your response
    don't hallucinate it can be costly
    be friendly and polite
    Go straight to the response and stop introducing your self except if the user greets you and stop there, respond to the greeting, introduce yourself and ask how you can assist otherwise 
    Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. 
    However, you are talking to a non-technical audience, so be sure to break down complicated concepts and 
    strike a friendly and converstional tone. If the passage is irrelevant to the answer, you may ignore it.
    
    QUESTION: {query}
    PASSAGE: {passage}
    CONVERSATION HISTORY: {history}
    """
    return prompt

def get_passage(prompt):
    """results = st.session_state.collection.query(
        query_texts=[prompt],
        n_results=5
    )
    passages = "\n".join(results["documents"][0])  # Combine passages
"""
    embed_fn.document_mode = False
    
    result = st.session_state.collection.query(query_texts=[prompt], n_results=5)
    
    [[passage]] =  [[" ".join([doc for sublist in result["documents"] for doc in sublist])]]
    
    return passage
    #return passages



def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)
if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = genai.GenerativeModel("gemini-1.5-flash-latest")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.history = st.session_state.history+"\nuser: {"+prompt+ "}"


    passage = get_passage(prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        print(st.session_state["gemini_model"])
        #prompt_template = f"your name if Futminna chatbot \nThis is the chat history below\n {st.session_state.history}\nBelow is the new prompt {prompt}"
        prompt_template = prepare_prompt(query = prompt, passage = passage, history = st.session_state.history)
        gen_output = st.session_state["gemini_model"].generate_content(prompt_template)
        stream = response_generator(gen_output.text)
        response = st.write_stream(stream)

        
    st.session_state.history = st.session_state.history+"\nuser: {"+prompt+ "}" +"\nFutminna chatbot: {"+ gen_output.text+ "}"
    st.session_state.messages.append({"role": "assistant", "content": response})
