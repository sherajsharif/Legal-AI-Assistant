# Legal Aid Bot (Groq-only, Free Deployable)

A modern legal assistant chatbot for India, powered by Llama 3 via Groq API. Supports chat, PDF upload for summary/draft, and PDF generation. No local models or vector DBs required—runs for free on Render, Railway, etc.

## Features
- Chat with Llama 3 (Groq API)
- Upload PDF for summary and legal draft
- Download legal draft as PDF
- Modern Streamlit frontend
- Free deployment (no GPU, no storage needed)

## Backend Setup
1. Clone the repo:
   ```bash
   git clone <your-repo-url>
   cd legal-aid-bot/backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in `backend/`:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
4. Run the backend:
   ```bash
   uvicorn main:app --reload
   ```

## Frontend Setup
1. Open a new terminal and go to the project root.
2. Run:
   ```bash
   streamlit run frontend/streamlit_app.py
   ```

## Deployment (Render Example)
- Push your code to GitHub.
- On Render, create a new Web Service:
  - Build command: `pip install -r requirements.txt`
  - Start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
  - Set environment variable: `GROQ_API_KEY`
  - Working directory: `backend`

## Environment Variables
- `GROQ_API_KEY`: Your Groq API key (get it from https://console.groq.com/keys)

## License
MIT 