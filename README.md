# FUTMinna-Chatbot

A Retrieval-Augmented Generation (RAG) chatbot designed to assist students of the **Federal University of Technology Minna (FUTMinna)**, Niger State, Nigeria.

This chatbot provides accurate, contextual answers to student queries based on the official FUTMinna Student Handbook. It uses vector embeddings to retrieve relevant passages and generates responses grounded in the handbook content, reducing hallucinations and ensuring reliability.

## Features

- **Interactive Chat Interface**: Built with Streamlit for a user-friendly experience.
- **Grounded Responses**: Retrieves relevant sections from the student handbook using ChromaDB and Gemini embeddings.
- **Conversation History**: Maintains chat history for contextual responses.
- **Streaming Responses**: Displays answers word-by-word for a natural feel.
- **Friendly & Detailed**: Responses are polite, comprehensive, and tailored for students (non-technical audience).

## Tech Stack

- **Streamlit**: For the web-based chat UI.
- **Google Generative AI (Gemini)**: 
  - `gemini-1.5-flash-latest` for response generation.
  - `text-embedding-004` for creating vector embeddings.
- **ChromaDB**: Local vector database for storing and querying handbook chunks.
- **Python Libraries**: `google.generativeai`, `chromadb`, `json`, `time`.

## Prerequisites

- Python 3.8+
- A Google API Key with access to Gemini models (free tier available via Google AI Studio).
- The student handbook text chunked into JSON format.

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/FUTMinna-Chatbot.git
   cd FUTMinna-Chatbot
   ```

2. **Install dependencies**:
   ```bash
   pip install streamlit google-generativeai chromadb
   ```

3. **Configure Gemini API Key**:
   - Replace the placeholder API key in the code with your own:
     ```python
     genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")
     ```
   - For security, consider using environment variables:
     ```python
     import os
     genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
     ```

## Preparing the Knowledge Base

The chatbot relies on a pre-chunked version of the FUTMinna Student Handbook stored as `chunked_text.json`.

### Source
Download the latest handbook from the official university website:  
[2023/2024 Session Students’ Handbook](https://futminna.edu.ng/wp-content/uploads/2024/06/2023-2024-Session-Student-Handbook-1-2.pdf)

### How to Create `chunked_text.json`
1. Extract text from the PDF (using tools like PyPDF2, pdfplumber, or LangChain's PDF loaders).
2. Chunk the text into manageable pieces (e.g., 500-1000 characters per chunk with overlap).
3. Save the list of text chunks as a JSON array:
   ```json
   ["chunk 1 text...", "chunk 2 text...", ...]
   ```

Example script snippet (using external libraries like LangChain for chunking):
```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = PyPDFLoader("handbook.pdf")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

chunk_texts = [doc.page_content for doc in chunks]
import json
with open("chunked_text.json", "w", encoding="utf-8") as f:
    json.dump(chunk_texts, f)
```

Place the generated `chunked_text.json` in the project root. On first run, the app will automatically embed and add these chunks to ChromaDB (stored locally in `./chroma_data`).

## Running the App

```bash
streamlit run app.py
```

(Replace `app.py` with the actual filename of your main script.)

Open the provided local URL in your browser and start chatting!

## Usage Tips

- Ask questions related to university policies, procedures, academic regulations, etc.
- The chatbot will only use information from the handbook — it ignores irrelevant passages.
- Greet it (e.g., "Hello") to get a friendly introduction.

## Limitations

- Responses are strictly grounded in the provided handbook version.
- Update `chunked_text.json` when a new handbook is released.
- Local ChromaDB persistence means embeddings are computed only once.

## Contributing

Contributions are welcome! Feel free to:
- Improve the prompt engineering.
- Add support for multiple/handbook versions.
- Enhance the UI or add features like file upload for updates.

Fork the repo, create a branch, and submit a pull request.

## License

MIT License — feel free to use and modify for educational purposes.

---

**Official University Website**: [https://futminna.edu.ng/](https://futminna.edu.ng/)

This project is unofficial and built to support FUTMinna students.
