import os
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatGroq
from langchain.chains import RetrievalQA

# Load environment variables from .env file
load_dotenv()

# Load vector database from disk
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma(
    persist_directory="data/chroma_db/human_rights_law",
    embedding_function=embedding
)

# Connect to Llama3 via Groq
llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=os.environ["GROQ_API_KEY"]
)

# Create the Retrieval QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=False
)

# Main function used by FastAPI
def ask_question(query):
    response = qa_chain.run(query)
    return response
