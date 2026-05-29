from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

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

if __name__ == '__main__':
    main()