from fastapi import FastAPI, Request, UploadFile
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import uvicorn
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import PyPDF2
from fastapi.responses import StreamingResponse
from fpdf import FPDF
import io

# Initialize FastAPI
load_dotenv()
app = FastAPI()

# Load the vector store from disk
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory="data/chroma_db/legal_rights", embedding_function=embedding)

# Load the Llama 3 model via Groq
llm = ChatGroq(
    groq_api_key=os.environ.get("GROQ_API_KEY"),
    model_name="llama3-70b-8192"
)

# Create a RAG Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectordb.as_retriever()
)

# Test route
@app.get("/")
def home():
    return {"message": "✅ Legal Assistant backend is running!"}

# POST endpoint to receive legal questions
@app.post("/query")
async def query(request: Request):
    try:
        body = await request.json()
        user_question = body.get("question")
        collection = body.get("collection", "legal_rights")  # default to legal_rights
        language = body.get("language", "auto")
        if not user_question:
            return {"error": "Please provide a 'question'"}

        # Dynamically load the vectorstore
        embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        base = "data/chroma_db"
        mapping = {
            "legal_rights": "legal_rights",
            "human_rights_law": "human_rights_law",
            "emergency": "emergency",
            "govt_schemes": "govt_schemes"
        }
        persist_directory = os.path.join(base, mapping.get(collection, "legal_rights"))
        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding
        )
        llm = ChatGroq(
            groq_api_key=os.environ.get("GROQ_API_KEY"),
            model_name="llama3-70b-8192"
        )
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectordb.as_retriever()
        )
        # Prompt wrapping
        if language == "hinglish":
            prompt = f"Answer the following question in Hinglish (Hindi written in Roman script): {user_question}"
        elif language == "hindi":
            prompt = f"Answer the following question in Hindi: {user_question}"
        elif language == "tamil":
            prompt = f"Answer the following question in Tamil: {user_question}"
        elif language == "bengali":
            prompt = f"Answer the following question in Bengali: {user_question}"
        elif language == "telugu":
            prompt = f"Answer the following question in Telugu: {user_question}"
        else:
            prompt = user_question
        answer = qa_chain.run(prompt)
        return {"answer": answer}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"Internal server error: {str(e)}"}

@app.post("/upload_doc")
async def upload_doc(file: UploadFile):
    try:
        # Read PDF content
        pdf_reader = PyPDF2.PdfReader(file.file)
        text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)
        if not text.strip():
            return {"summary": "No text found in PDF.", "draft": "No draft generated."}
        # Summarize
        summary_prompt = f"Summarize the following document in 5 lines:\n{text}"
        summary = qa_chain.run(summary_prompt)
        # Generate RTI/FIR draft
        draft_prompt = f"Based on the following complaint/notes, generate a legal draft suitable for an RTI or FIR application.\nDocument:\n{text}"
        draft = qa_chain.run(draft_prompt)
        return {"summary": summary, "draft": draft}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"summary": "Error processing document.", "draft": str(e)}

@app.post("/generate_pdf")
async def generate_pdf(data: dict):
    draft = data.get("draft", "")
    if not draft.strip():
        return {"error": "No draft provided."}
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in draft.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return StreamingResponse(pdf_output, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=legal_draft.pdf"})

# Optional: Run server from here directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
