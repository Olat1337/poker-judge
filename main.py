from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def main():
    loader = PyPDFLoader("data/rules.pdf")
    pages = loader.load()
    print(len(pages))

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(pages)
    print(len(chunks))
    print(chunks[0].page_content)

    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(chunks, embedding_model)

    query = "What happens if I bet a single oversized chip?"

    docs = db.similarity_search(query)
    print(docs[0].page_content)
if __name__ == '__main__':
    main()