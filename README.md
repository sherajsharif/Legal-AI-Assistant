# ⚖️ GenAI Legal Assistant (India)

A modern, AI-powered legal aid bot for India. Ask questions about your legal rights, government schemes, emergencies, or human rights in English, Hindi, Hinglish, and more. Upload complaints/notes for instant RTI/FIR draft generation. Powered by Llama 3 + Groq, ChromaDB, and Streamlit.

---

## 🚀 Features

- **Conversational Q&A**: Ask legal questions in multiple languages (English, Hindi, Hinglish, Tamil, Bengali, Telugu, etc.)
- **Retrieval-Augmented Generation (RAG)**: Answers are grounded in Indian legal documents and government schemes using ChromaDB.
- **Document Uploader**: Upload a PDF complaint/notes and get a summary + auto-generated RTI/FIR draft.
- **Download as PDF**: Instantly download generated legal drafts.
- **Voice Input & TTS**: (Optional) Speak your question and listen to the answer.
- **Smart Pre-filled Questions**: Click to auto-fill common legal queries.
- **Query History**: See and copy your last 5 Q&A pairs.
- **Emergency Help**: Quick access to helplines and hospital locator.
- **Modern UI**: Light/dark mode, expert mode, beautiful sidebar, and more.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **LLM**: [Llama 3 (Groq API)](https://groq.com/)
- **Vector DB**: [ChromaDB](https://www.trychroma.com/)
- **Embeddings**: [HuggingFace MiniLM](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- **PDF**: [PyPDF2](https://pypi.org/project/PyPDF2/), [fpdf](https://pypi.org/project/fpdf/)
- **TTS**: [gTTS](https://pypi.org/project/gTTS/)
- **Voice**: [streamlit-webrtc](https://github.com/whitphx/streamlit-webrtc), [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)

---

## 📦 Setup & Installation

1. **Clone the repo:**
   ```sh
   git clone https://github.com/yourusername/legal-aid-bot.git
   cd legal-aid-bot
   ```
2. **Create a virtual environment:**
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r backend/requirements.txt
   ```
4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in your API keys:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     DETECTLANGUAGE_API_KEY=your_detectlanguage_key_here
     ```
5. **Prepare data:**
   - Ensure `data/legal_docs/` contains your legal documents.
   - Run the embedding script to build the vectorstore:
     ```sh
     python backend/chromadb_setup.py
     ```

---

## 🖥️ Running the App

1. **Start the backend (FastAPI):**
   ```sh
   uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
   ```
2. **Start the frontend (Streamlit):**
   ```sh
   streamlit run frontend/streamlit_app.py
   ```
3. **Open your browser:**
   - Go to [http://localhost:8501](http://localhost:8501) for the frontend.
   - Backend API is at [http://localhost:8000](http://localhost:8000)

---

## 🌐 Deployment

- **.env**: Never commit your `.env` file. Set environment variables securely on your server/platform.
- **Data**: Upload your `data/chroma_db/` and legal docs to the server.
- **Ports**: Expose 8000 (FastAPI) and 8501 (Streamlit) as needed.
- **System dependencies**: Some packages (e.g., `av`, `PyPDF2`) may require system libraries (like ffmpeg).
- **Multi-service**: Use a process manager or platform that supports multiple services if deploying both frontend and backend.

---

## 📁 Project Structure

```
legal-aid-bot/
  backend/
    main.py
    chromadb_setup.py
    ...
  frontend/
    streamlit_app.py
  data/
    legal_docs/
    chroma_db/
  models/
  deployment/
  ...
```

---

## 📝 Credits & License

- Built by [Sheraj Sharif](https://github.com/sherajsharif)
- Powered by open-source and the Indian legal community
- MIT License

---

## 🙏 Acknowledgements

- [Groq](https://groq.com/) for blazing-fast Llama 3 API
- [LangChain](https://python.langchain.com/) for RAG and chaining
- [ChromaDB](https://www.trychroma.com/) for vector search
- [Streamlit](https://streamlit.io/) for rapid UI
- [HuggingFace](https://huggingface.co/) for embeddings
- [PyPDF2](https://pypi.org/project/PyPDF2/), [fpdf](https://pypi.org/project/fpdf/) for PDF handling
- [gTTS](https://pypi.org/project/gTTS/) for TTS
- [streamlit-webrtc](https://github.com/whitphx/streamlit-webrtc) for voice input

---

> **Empowering every Indian with accessible legal knowledge.** 