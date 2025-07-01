from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import os

# Load the PDF
pdf_path = "data\pdfs\human_rights_guide.pdf"
loader = PyMuPDFLoader(pdf_path)
documents = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = splitter.split_documents(documents)

# Load embedding model
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Define vector DB path
persist_dir = "data/chroma_db/human_rights_law"
os.makedirs(persist_dir, exist_ok=True)

# Create vector store
vectorstore = Chroma.from_documents(docs, embedding=embedding, persist_directory=persist_dir)
vectorstore.persist()

print("✅ Human Rights PDF loaded and saved in ChromaDB.")
