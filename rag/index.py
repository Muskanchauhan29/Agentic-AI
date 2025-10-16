from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
 
pdf_path = Path(__file__).parent / "book.pdf"

loader = PyPDFLoader(file_path = pdf_path)
docs = loader.load()

# print(docs[12])
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 400
)
chunks = text_splitter.split_documents(documents=docs)

