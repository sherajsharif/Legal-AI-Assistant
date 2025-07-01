from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os

# Step 1: Load your text file
loader = TextLoader("data/legal_docs/legal_rights.txt", encoding='utf-8')
documents = loader.load()

# Step 2: Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# Step 3: Load the embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Step 4: Create ChromaDB folder if not exists
persist_dir = "data/chroma_db/legal_rights"
os.makedirs(persist_dir, exist_ok=True)

# Step 5: Create vector store and persist it
vectorstore = Chroma.from_documents(documents=docs, embedding=embedding_model, persist_directory=persist_dir)
vectorstore.persist()

print("✅ legal_rights data loaded and saved in ChromaDB.")
