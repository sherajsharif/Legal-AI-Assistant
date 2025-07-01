from fastapi import FastAPI, Request, UploadFile
from langchain_groq import ChatGroq
import os
import PyPDF2
from fastapi.responses import StreamingResponse
from fpdf import FPDF
import io

app = FastAPI()

@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        body = await request.json()
        prompt = body.get("prompt")
        groq_api_key = os.getenv("GROQ_API_KEY")
        llm = ChatGroq(
            api_key=groq_api_key,
            model="llama3-8b-8192"
        )
        response = llm.invoke(prompt)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

@app.post("/upload_doc")
async def upload_doc(file: UploadFile):
    try:
        # Read PDF content
        pdf_reader = PyPDF2.PdfReader(file.file)
        text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)
        if not text.strip():
            return {"summary": "No text found in PDF.", "draft": "No draft generated."}
        # Summarize
        groq_api_key = os.getenv("GROQ_API_KEY")
        llm = ChatGroq(
            api_key=groq_api_key,
            model="llama3-8b-8192"
        )
        summary_prompt = f"Summarize the following document in 5 lines:\n{text}"
        summary = llm.invoke(summary_prompt)
        # Generate RTI/FIR draft
        draft_prompt = f"Based on the following complaint/notes, generate a legal draft suitable for an RTI or FIR application.\nDocument:\n{text}"
        draft = llm.invoke(draft_prompt)
        return {"summary": summary, "draft": draft}
    except Exception as e:
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
