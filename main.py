from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

PDF_FILE_PATH = "data/rules.pdf"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
LLM_MODEL = "llama3"

def setup_llm(llm_model):
    llm = Ollama(model=llm_model)
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
    print("CHECK FIRST CHUNK:")
    print(chunks[0].page_content)
    return chunks

def create_vector_db(chunks, embedding_model_name):
    print("CREATING VECTOR DB")
    embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)
    db = Chroma.from_documents(chunks, embedding_model)

    return db
def main():
    chunks = load_split_pdf(PDF_FILE_PATH)
    db = create_vector_db(chunks, EMBEDDING_MODEL_NAME)

    #"TEST SEARCH"
    query = "What happens if I bet a single oversized chip?"
    print(f"SEARCHING ANSWER TO THE QUESTION: {query}")
    docs = db.similarity_search(query)
    print("FOUND RULE")
    print(docs[0].page_content)

    llm = setup_llm(LLM_MODEL)

    print("SENDING TEST REQUEST TO LLM")
    response = llm.invoke("Hello! Are you ready to act as a poker judge?")
    print(response)
    
if __name__ == '__main__':
    main()