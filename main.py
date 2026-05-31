from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

PDF_FILE_PATH = "data/rules.pdf"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
LLM_MODEL = "llama3"
CHROMA_PATH = "chroma_db"

def ask_judge(question, db, llm, chat_history =""):
    docs = db.similarity_search(question, k=5)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
        You are a professional and helpful poker tournament judge.

        [HISTORY]
        {chat_history}

        [RULES]
        {context}

        INSTRUCTIONS:
        1. Answer the player's question naturally and directly.
        2. If the question is about poker, base your answer strictly on the [RULES].
        3. If the question is about previous messages or the player, use the [HISTORY].
        4. If the answer is not in the history or rules, simply say "I don't know."
        5. CRITICAL: NEVER mention the words "[RULES]", "[HISTORY]", or explain how you found the information. Do not explain your thought process. Just provide the final answer.
        6. If the player is just greeting you or talking about themselves (not asking a poker question), DO NOT quote the rules or invent game scenarios. Just reply politely and conversationally.        
        
        Player: {question}
        Judge:
        """

    response = llm.invoke(prompt)

    return response

def setup_llm(llm_model):
    llm = OllamaLLM(model=llm_model)

    return llm

def load_split_pdf(file_path):
    print("LOADING AND SPLITTING PDF")
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    print("PAGES IN PDF: "+str(len(pages)))

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(pages)
    print("AMOUNT OF CHUNKS: "+ str(len(chunks)))

    return chunks

def main():
    llm = setup_llm(LLM_MODEL)
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    if os.path.isdir(CHROMA_PATH):
        print("LOADING DB FROM DISK...")
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_model)
    else:
        print("CREATING NEW DB...")
        chunks = load_split_pdf(PDF_FILE_PATH)
        db = Chroma.from_documents(chunks, embedding_model, persist_directory=CHROMA_PATH)

    print("\n--- POKER JUDGE IS READY ---")
    print("Type 'exit' to close the program.\n")

    messages = []

    while True:
        question = input("You:")

        if question.lower() == "exit":
            break

        print("---THINKING---")

        last_chat_history = "\n".join(messages[-4:])

        response = ask_judge(question, db, llm, last_chat_history)

        print("JUDGE'S VERDICT: ")
        print(response+"\n")

        messages.append(f"Player: {question}")
        messages.append(f"Judge: {response}")

if __name__ == '__main__':
    main()