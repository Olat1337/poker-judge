# 🃏 Poker Tournament Judge AI

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-⚡-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-white.svg)

An AI-powered strict and fair poker referee. This project uses **RAG (Retrieval-Augmented Generation)** architecture to answer any tricky questions about poker rules based strictly on the official rulebook. 

It never hallucinates: if the answer is not in the rules, the judge will honestly state that it does not know.

## 🧠 Architecture (RAG Pipeline)
1. **Document Loader:** Parses the official Poker Rules PDF.
2. **Text Splitter:** Chunks the document into manageable pieces with overlap to preserve context.
3. **Embeddings:** Uses HuggingFace `all-MiniLM-L6-v2` to convert text chunks into vector representations.
4. **Vector Database:** Stores vectors locally using **ChromaDB** for instant semantic search.
5. **LLM Engine:** Uses **Llama 3** (via local Ollama) to generate the final verdict based *only* on the retrieved context.

## 🚀 Features
* **Smart Loading:** The vector database is cached on the local drive (`/chroma_db`) for instant startup.
* **CLI Version:** Continuous interactive chat in the terminal (`main.py`).
* **Web GUI:** Beautiful and modern web interface powered by Streamlit (`gui.py`).
* **100% Local & Private:** No API keys, no paid subscriptions. Runs entirely on your machine.

## ⚙️ Installation & Setup

1. **Install Ollama** and download the Llama 3 model:
   ```bash
   ollama run llama3
   ```

2. Clone the repository and install dependencies:
     ```bash
     git clone https://github.com/Olat1337/poker-judge.git
     cd poker_judge
     pip install -r requirements.txt
     ```
3. Run the initial setup (CLI version):
   On the first run, this will parse the PDF and create the ChromaDB vector storage.
   ```bash
   python main.py
   ```
## 💻 Usage

## Launch the Web Interface:
  ```bash
  streamlit run gui.py
  ```
Open your browser and go to http://localhost:8501.
## 🔜 Roadmap (Coming Soon)
[ ] Telegram Bot Integration: Bring the AI Judge to your pocket via aiogram.

[ ] Conversational Memory: Allow the judge to remember context from previous questions in the same session.
