from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

PDF_FILE_PATH = "data/rules.pdf"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
LLM_MODEL = "llama3"
CHROMA_PATH = "chroma_db"

def ask_judge(query, db, llm):
    docs = db.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    template_text = """You are a strict poker tournament judge. Answer the player's question using ONLY the provided rules. If the answer is not in the rules, say "I don't know".

    Rules:
    {context}

    Question: {question}

    Answer:"""

    template = PromptTemplate.from_template(template_text)
    final_prompt = template.format(context=context, question = query)
    response = llm.invoke(final_prompt)

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

    while True:
        query = input()
        if query == "exit":
            break
        print("---THINKING---")
        response = ask_judge(query, db, llm)

        print("JUDGE'S VERDICT: ")
        print(response)

if __name__ == '__main__':
    main()