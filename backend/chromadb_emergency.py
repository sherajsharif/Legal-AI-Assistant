from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
import os

# Load emergency data
loader = TextLoader("data/legal_docs/emergency_help.txt")
documents = loader.load()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# Load embedding model
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Setup ChromaDB directory
persist_dir = "data/chroma_db/emergency"
os.makedirs(persist_dir, exist_ok=True)

# Store in vector database
vectorstore = Chroma.from_documents(documents=docs, embedding=embedding, persist_directory=persist_dir)
vectorstore.persist()

print("✅ emergency_help data loaded and saved in ChromaDB.")
