# 🃏 Poker Tournament Judge AI: Local RAG Rule Enforcer

A local AI application that serves as a poker referee, answering user questions and resolving disputes based strictly on the official Poker Tournament Directors Association (TDA) rulebook.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-green.svg?logo=langchain)](https://python.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg?logo=streamlit)](https://streamlit.io/)
[![aiogram](https://img.shields.io/badge/aiogram-3.4+-2CA5E0.svg?logo=telegram)](https://aiogram.dev/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-white.svg?logo=ollama)](https://ollama.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F00.svg)](https://www.trychroma.com/)

## 🔗 Interfaces
* **Web UI:** Web interface powered by Streamlit.
<img width="1920" height="1080" alt="Poker Judge WEB UI GIF" src="https://github.com/user-attachments/assets/227d0b6d-8df8-4af6-9fda-4267f2935706" />

* **Telegram Bot:** Asynchronous bot with multi-user memory isolation.
<img width="1920" height="1080" alt="Poker Judge TELEGRAM GIF" src="https://github.com/user-attachments/assets/61ae36d3-5bc4-4978-b002-0569e72b46cd" />

* **CLI:** Interactive chat directly in the terminal.

## 🎯 Project Overview
I built this project to explore Retrieval-Augmented Generation (RAG) architectures and local LLM deployment. 

Resolving disputes during a poker tournament requires consistent application of complex rules. This system ingests the official TDA rulebook and uses RAG to retrieve the exact relevant rules before passing them to the language model to answer situational questions.

## 🛠️ Technology Stack & Architecture Decisions

I designed this system to be completely offline and privacy-focused, requiring no external API keys.

### RAG Engine & Data
* **Framework:** LangChain.
* **Vector Store:** ChromaDB.
* **Embeddings:** HuggingFace `all-MiniLM-L6-v2`.
* **Why this stack:** LangChain provides standard abstractions for connecting document loaders, text splitters, and vector stores. I chose ChromaDB because it runs locally and persists data to disk easily. The `MiniLM` embedding model was chosen because it is lightweight and runs fast on CPU.

### Generative AI
* **LLM:** Llama 3 (via Ollama).
* **Why local inference:** I selected local inference via Ollama over cloud APIs (like OpenAI) to keep the system fully offline, private, and free of per-request costs. It ensures the application can run entirely locally without internet dependency.

### Interfaces
* **Telegram Bot:** Built with `aiogram`.
* **Web UI:** Built with Streamlit.
* **Why decouple them:** I isolated the core RAG logic in `main.py` so that multiple interfaces (CLI, Streamlit, and Telegram) can import and interact with the exact same retrieval pipeline without duplicating code.

## 📊 RAG Pipeline Workflow

Before generating an answer, the AI follows a strict retrieval pipeline:

1. **Document Loading:** Parses the raw `rules.pdf` using PyPDF.
2. **Text Splitting:** Utilizes a `RecursiveCharacterTextSplitter` (chunk size: 1000, overlap: 200). *Why:* This breaks the rulebook into searchable pieces while keeping sentences and paragraphs intact via the overlap.
3. **Vector Search:** Queries ChromaDB to find the top 5 most semantically relevant rule chunks.
4. **Prompting:** The retrieved rules, along with the user's recent chat history, are injected into a strict prompt. The prompt explicitly instructs the model to refuse to answer if the provided context does not contain the information.

## 📁 Repository Structure

    ├── chroma_db/                 # Persistent local vector database storage (ignored in git)
    ├── data/
    │   └── rules.pdf              # The official TDA Poker Rulebook
    ├── .env                       # Environment variables (Telegram token)
    ├── .gitignore                 
    ├── gui.py                     # Streamlit frontend user interface
    ├── main.py                    # Core RAG logic, Chroma setup, and CLI interface
    ├── requirements.txt           # Environment dependencies
    └── tg_bot.py                  # Asynchronous Telegram bot implementation

## 📈 System Capabilities

* **Conversational Memory:** The system retains the last 4 messages in memory. *Why:* This allows users to ask natural follow-up questions (e.g., "What if he raised instead?") without needing to restate the entire scenario.
* **Multi-Tenant Isolation:** The Telegram bot uses a local dictionary to isolate chat histories by `user_id`. *Why:* This ensures that multiple users querying the bot simultaneously do not cross-contaminate each other's context windows.

## 🚀 How to Run Locally

### 1. Install Ollama & Pull the Model
You must have [Ollama](https://ollama.com/) installed and running on your system. Pull the required Llama 3 model in your terminal:

    ollama run llama3

### 2. Clone the repository and install dependencies
Run the following commands in your terminal:

    git clone https://github.com/Olat1337/poker-judge.git
    cd poker-judge
    pip install -r requirements.txt

### 3. Initialize the Vector Database (First Run)
Run the core script once to parse the PDF, generate embeddings, and build the `chroma_db` directory. You can test the chat in the terminal or type `exit` to close it.

    python main.py

### 4. Launch Your Preferred Interface

**To run the Web UI:**

    streamlit run gui.py

*(The UI will automatically open in your browser at http://localhost:8501)*

**To run the Telegram Bot:**
1. Create a `.env` file in the root directory and add your bot token: `TELEGRAM_TOKEN=your_bot_token_here`
2. Start the bot:

    python tg_bot.py
