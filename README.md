# 🃏 Poker Tournament Judge AI: RAG-Powered Rule Enforcer

An end-to-end local AI application that serves as a strict, hallucination-free poker referee, predicting and rendering official rulings based purely on tournament rulebooks.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-green.svg?logo=langchain)](https://python.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg?logo=streamlit)](https://streamlit.io/)
[![aiogram](https://img.shields.io/badge/aiogram-3.4+-2CA5E0.svg?logo=telegram)](https://aiogram.dev/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-white.svg?logo=ollama)](https://ollama.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F00.svg)](https://www.trychroma.com/)

## 🔗 Interfaces
* **Web UI:** Modern chat interface powered by Streamlit.
* **Telegram Bot:** Fully asynchronous bot with multi-user memory isolation.
* **CLI:** Continuous interactive chat directly in the terminal.
## 🎯 Project Overview
Resolving disputes during a poker tournament can be stressful, and ensuring consistent application of the rules is a constant challenge for human floor staff. **Poker Tournament Judge AI** solves this by ingesting the official Poker Tournament Directors Association (TDA) rulebook and using a Retrieval-Augmented Generation (RAG) architecture to answer complex situational questions.

This project was built to demonstrate a complete, production-ready local AI lifecycle-from document chunking and vector embeddings to conversational memory and multi-platform deployment (Web, CLI, and Telegram). It guarantees zero hallucinations: if the answer isn't in the rulebook, the judge will honestly state that it does not know.

## 🛠️ Full Technology Stack

To ensure strict factual accuracy and fast performance while keeping data 100% private, the application utilizes a modern Python AI ecosystem and a decoupled interface architecture.

### RAG Engine & Data Engineering
* **LangChain:** Orchestrates the entire retrieval pipeline, prompt templating, and model chaining.
* **HuggingFace Embeddings (`all-MiniLM-L6-v2`):** Converts text chunks into dense mathematical vector representations.
* **ChromaDB:** A persistent local vector database used for instant semantic search and context retrieval.
* **PyPDF:** Parses and extracts raw text from the official `rules.pdf`.

### Generative AI (LLM)
* **Ollama (Llama 3):** Powers the conversational brain of the application locally, removing the need for paid cloud API keys (like OpenAI) and ensuring complete privacy.

### Full-Stack Architecture
* **Telegram Backend (`aiogram`):** A high-performance, asynchronous routing engine managing stateful user sessions and chat histories.
* **Presentation Layer (Streamlit):** A responsive, cached web interface (`gui.py`) providing a clean chat experience.

## 📊 RAG Pipeline & Data Workflow

Before generating an answer, the AI follows a strict data retrieval pipeline to prevent hallucination:

* **Document Loading:** Parses the raw `rules.pdf` located in the `data/` directory.
* **Text Splitting:** Utilizes a `RecursiveCharacterTextSplitter` (1000 chunk size, 200 overlap) to break the rulebook into manageable pieces without losing contextual meaning.
* **Vector Search:** When a user asks a question, the system queries ChromaDB to find the top 5 most semantically relevant rule chunks.
* **Prompt Injection:** The retrieved rules, along with the user's recent chat history, are injected into a highly constrained prompt.
* **Final Verdict:** The Llama 3 model processes the prompt and outputs a natural, direct ruling based *only* on the injected rules.

## 📁 Repository Structure

```text
├── chroma_db/                 # Persistent local vector database storage
├── data/
│   └── rules.pdf              # The official TDA Poker Rulebook
├── .env                       # Environment variables (Telegram token)
├── .gitignore                 # Configures files and directories to ignore in Git
├── gui.py                     # Streamlit frontend user interface
├── main.py                    # RAG logic, Chroma setup, and CLI interface
├── requirements.txt           # Frozen production dependencies
├── tg_bot.py                  # Asynchronous Telegram bot implementation
└── README.md                  # Project documentation
(Note: Chroma db data are intentionally git-ignored to maintain clean version control hygiene).
```

## 📈 System Capabilities & Constraints
Conversational Memory: The AI remembers the context of the conversation up to the last 4 messages, allowing for natural follow-up questions without losing context.

Hallucination Prevention: Strict prompting forces the LLM to output "I don't know" rather than inventing game scenarios if the context is missing.

Multi-Tenant Isolation: The Telegram bot uses a local dictionary to isolate users_history, ensuring different players querying the bot simultaneously do not cross-contaminate each other's chat histories.

## 🚀 How to Run Locally
If you would like to run this application on your own machine, follow these steps:

1. Install Ollama & Pull the Model
You must have Ollama installed and running on your system. Pull the required Llama 3 model:
```Bash
ollama run llama3
```
2. Clone the repository and install dependencies

```Bash
git clone https://github.com/Olat1337/poker-judge.git
cd poker-judge
pip install -r requirements.txt
```
3. Initialize the Vector Database (First Run)
Run the CLI version once to parse the PDF and build the chroma_db directory. You can chat in the terminal or type exit to close it.

```Bash
python main.py
```
4. Launch Your Preferred Interface

To run the Web UI:
```Bash
streamlit run gui.py
```
(The UI will automatically open in your browser at http://localhost:8501).

To run the Telegram Bot:

First, create a .env file in the root directory and add your bot token:

TELEGRAM_TOKEN=your_bot_token_here
Then start the bot:

```Bash
python tg_bot.py
```