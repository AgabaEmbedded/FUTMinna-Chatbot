# FUTMinna-Chatbot

A **Retrieval-Augmented Generation (RAG)** chatbot designed to assist students of the **Federal University of Technology Minna (FUTMinna)**, Niger State, Nigeria.

<p align="center">
  <a href="https://futminna-chatbot.streamlit.app/">
    <img src="Demo.png" width="100" />
  </a>
</p>

The chatbot provides accurate, contextual, and detailed answers based **exclusively** on the official FUTMinna Student Handbook. It uses vector search to retrieve relevant sections and generates reliable responses with minimal hallucination.

## Features

- Clean, modern **Streamlit chat interface**
- **Grounded responses** using relevant handbook passages retrieved via ChromaDB
- **Streaming responses** for a natural conversation feel
- Persistent local vector database (embeddings computed only once)
- Friendly, polite, and detailed tone tailored for students
- Secure API key handling via environment variables
- Uses the latest Gemini model for speed and quality

## Tech Stack

- **Streamlit** – Interactive web UI
- **Google Generative AI**  
  - `gemini-1.5-flash-002` (latest Flash model as of 2026) for response generation  
  - `text-embedding-004` for vector embeddings
- **ChromaDB** – Local persistent vector database
- Python 3.8+

## Prerequisites

- Python 3.8 or higher
- A Google API key with access to Gemini models (obtain from [Google AI Studio](https://aistudio.google.com/))
- Pre-chunked student handbook in JSON format (`chunked_text.json`)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/FUTMinna-Chatbot.git
   cd FUTMinna-Chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Gemini API key**
   
   Recommended: Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   
   Or export it in your terminal:
   ```bash
   export GEMINI_API_KEY="your_actual_api_key_here"
   ```

## Preparing the Knowledge Base

The chatbot requires `chunked_text.json` containing text chunks from the official student handbook.

### Source
Latest handbook:  
[2023/2024 Session Students’ Handbook](https://futminna.edu.ng/wp-content/uploads/2024/06/2023-2024-Session-Student-Handbook-1-2.pdf)  
*(Update the source when a newer version is released)*

### Generating `chunked_text.json`

You can use any PDF-to-text + chunking method. Example using LangChain (optional):

```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

loader = PyPDFLoader("handbook.pdf")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

chunk_texts = [doc.page_content for doc in chunks]

with open("chunked_text.json", "w", encoding="utf-8") as f:
    json.dump(chunk_texts, f, ensure_ascii=False, indent=2)
```

Place `chunked_text.json` in the project root directory.

On first run, the app will automatically embed all chunks into the local ChromaDB database (stored in `./chroma_data`).

## Running the Chatbot

```bash
streamlit run app.py
```

Open the local URL shown in your browser and start asking questions!

## Usage Tips

- Ask about academic regulations, registration procedures, hostel rules, examination policies, etc.
- The bot only uses information from the loaded handbook.
- Greet it with "hi" or "hello" for a friendly introduction.
- Responses are detailed and student-friendly.

## Project Structure

```
.
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── chunked_text.json       # Handbook text chunks (you provide)
├── chroma_data/            # Auto-created: persistent vector database
└── .env                    # Optional: your API key (gitignored)
```

## Limitations

- Answers are limited to the content and version of the handbook provided.
- Update `chunked_text.json` whenever a new handbook is released.
- Runs locally – no external server required.

## Contributing

Contributions are welcome! Ideas for improvement:

- Support for multiple handbook versions
- PDF upload interface for easy updates
- Clear chat / session reset button
- Export chat history
- Better UI styling

Feel free to fork, create a branch, and submit a pull request.

## License

MIT License – Free to use, modify, and distribute for educational purposes.

---

**Official University Website**: [https://futminna.edu.ng/](https://futminna.edu.ng/)

*This is an unofficial student-support project built to help the FUTMinna community.* 

Enjoy chatting with your handbook-powered assistant!