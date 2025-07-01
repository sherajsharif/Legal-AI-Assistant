import streamlit as st
import requests
from gtts import gTTS
import tempfile
import os
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import av
import numpy as np
import speech_recognition as sr

# --- Custom CSS for modern look ---
st.markdown('''
    <style>
    body {
        background: linear-gradient(135deg, #232526 0%, #414345 100%);
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 900;
        color: #fffbe7;
        margin-bottom: 0.2em;
        letter-spacing: -1px;
        text-shadow: 0 2px 12px #000, 0 1px 0 #fffbe7;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #f5f7fa;
        margin-bottom: 1.5em;
        text-shadow: 0 1px 8px #000;
    }
    .answer-card {
        background: #232526cc;
        border-radius: 1.2em;
        box-shadow: 0 4px 24px 0 rgba(34, 139, 230, 0.08);
        padding: 2em 1.5em;
        margin-top: 1.5em;
        margin-bottom: 1.5em;
        font-size: 1.15rem;
        color: #f5f7fa;
    }
    .footer {
        color: #e2e8f0;
        font-size: 0.95rem;
        margin-top: 2em;
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(90deg, #3a8dde 0%, #6dd5ed 100%);
        color: white;
        font-weight: 600;
        border-radius: 0.7em;
        padding: 0.6em 2em;
        border: none;
        margin-top: 1em;
        transition: background 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #6dd5ed 0%, #3a8dde 100%);
    }
    .stTextInput>div>div>input {
        border-radius: 0.7em;
        border: 1.5px solid #3a8dde;
        padding: 0.7em;
        font-size: 1.1rem;
        color: #f5f7fa;
        background: #232526;
    }
    label, .stTextInput label, .stTextInput>label {
        color: #e2e8f0 !important;
    }
    </style>
''', unsafe_allow_html=True)

# --- Sidebar for language and knowledge base selection ---
st.sidebar.image("https://img.icons8.com/ios-filled/100/2d3748/scales.png", width=60)
st.sidebar.markdown("<h2 style='color:#fff;letter-spacing:0.5px;text-shadow:0 2px 8px #000;font-weight:900;'>Settings</h2>", unsafe_allow_html=True)

# --- Theme Toggle ---
theme = st.sidebar.toggle("🌗 Light/Dark Mode", value=True)
if theme:
    main_bg = "linear-gradient(135deg, #232526 0%, #414345 100%)"
    card_bg = "#232526cc"
    text_color = "#fffbe7"
    subtitle_color = "#f5f7fa"
else:
    main_bg = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
    card_bg = "#fff"
    text_color = "#2d3748"
    subtitle_color = "#4a5568"
st.markdown(f'''
    <style>
    body {{
        background: {main_bg};
    }}
    .main-header {{
        font-size: 2.5rem;
        font-weight: 900;
        color: {text_color};
        margin-bottom: 0.2em;
        letter-spacing: -1px;
        text-shadow: 0 2px 12px #000, 0 1px 0 {text_color};
    }}
    .subtitle {{
        font-size: 1.1rem;
        color: {subtitle_color};
        margin-bottom: 1.5em;
        text-shadow: 0 1px 8px #000;
    }}
    .answer-card {{
        background: {card_bg};
        border-radius: 1.2em;
        box-shadow: 0 4px 24px 0 rgba(34, 139, 230, 0.08);
        padding: 2em 1.5em;
        margin-top: 1.5em;
        margin-bottom: 1.5em;
        font-size: 1.15rem;
        color: {text_color};
    }}
    .chat-bubble-q {{
        background: #3a8dde;
        color: #fff;
        border-radius: 1.2em 1.2em 1.2em 0.3em;
        padding: 1em 1.2em;
        margin: 0.5em 0 0.2em 0;
        max-width: 80%;
        font-size: 1.08em;
        align-self: flex-end;
    }}
    .chat-bubble-a {{
        background: {card_bg};
        color: {text_color};
        border-radius: 1.2em 1.2em 0.3em 1.2em;
        padding: 1em 1.2em;
        margin: 0.2em 0 0.5em 0;
        max-width: 80%;
        font-size: 1.08em;
        align-self: flex-start;
        border: 1.5px solid #3a8dde22;
    }}
    .footer {{
        color: {subtitle_color};
        font-size: 0.95rem;
        margin-top: 2em;
        text-align: center;
    }}
    </style>
''', unsafe_allow_html=True)

# --- Expert Mode Toggle ---
expert_mode = st.sidebar.toggle("💼 Legal Expert Mode", value=False)

languages = {
    "Auto Detect": "auto",
    "English": "english",
    "Hindi": "hindi",
    "Hinglish": "hinglish",
    "Tamil": "tamil",
    "Bengali": "bengali",
    "Telugu": "telugu"
}
selected_language = st.sidebar.selectbox("Select language:", list(languages.keys()))
language_key = languages[selected_language]

collections = {
    "Legal Rights": "legal_rights",
    "Human Rights Law": "human_rights_law",
    "Emergency": "emergency",
    "Government Schemes": "govt_schemes"
}
selected_collection = st.sidebar.selectbox("Select knowledge base:", list(collections.keys()))
collection_key = collections[selected_collection]

# --- Emergency Help Section (moved below language and knowledge base selection) ---
st.sidebar.markdown('''
<div style="background:linear-gradient(90deg,#3a8dde 0%,#a259c6 100%);padding:1.5em 1.2em 1.2em 1.2em;border-radius:1.3em;margin-bottom:1.7em;box-shadow:0 4px 18px #3a8dde33;">
  <div style="font-size:1.4em;font-weight:700;color:#fff;letter-spacing:0.5px;">🚨 Emergency Help</div>
  <ul style="list-style:none;padding-left:0;margin:1.2em 0 0 0;font-size:1.12em;">
    <li>👮‍♂️ Police: <b>100</b></li>
    <li>👩‍🦰 Women Helpline: <b>1091</b></li>
    <li>🚑 Ambulance: <b>102</b></li>
    <li>🧒 Child Helpline: <b>1098</b></li>
  </ul>
  <a href="https://www.google.com/maps/search/hospitals" target="_blank" style="color:#fff;text-decoration:underline;font-weight:600;">🏥 Find Nearby Hospitals</a>
  <br><br>
  <button onclick="window.location.href='tel:100'" style="background:#fff;color:#3a8dde;font-weight:700;padding:0.7em 1.3em;border:none;border-radius:0.8em;font-size:1.15em;cursor:pointer;margin-top:1.2em;box-shadow:0 2px 8px #3a8dde22;">Panic Help</button>
</div>
''', unsafe_allow_html=True)

st.markdown('<div class="main-header" style="font-family:Inter,Roboto,sans-serif;font-size:2.5em;font-weight:800;letter-spacing:0.5px;color:#fffbe7;margin-bottom:0.2em;">⚖️ GenAI Legal Assistant (India)</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle" style="font-size:1.15em;color:#b0b8c1;font-weight:500;margin-bottom:2.2em;">Ask questions about your legal rights, government schemes, emergencies, or human rights. Powered by Llama 3 + Groq.</div>', unsafe_allow_html=True)

with st.container():
    query = st.text_input("❓ Your Legal Question", st.session_state.get("prefill_query", ""), key="question_input")
    ask_btn = st.button("Ask", use_container_width=True)

    # --- Sample Questions ---
    st.markdown('<div style="margin-top:1.2em; font-size:1.02em; color:#b0b8c1;font-weight:600;">Try asking:</div>', unsafe_allow_html=True)
    sample_questions = [
        ("What are my rights during arrest?", "English"),
        ("FIR दर्ज करने की प्रक्रिया क्या है?", "Hindi"),
        ("Arrest ke time mere kya rights hain?", "Hinglish"),
        ("How do I file an RTI?", "English"),
        ("मुफ्त कानूनी सहायता कैसे प्राप्त करें?", "Hindi"),
        ("Free legal aid kaise milegi?", "Hinglish"),
        ("What is Article 21?", "English")
    ]
    cols = st.columns(len(sample_questions))
    for i, (q, lang) in enumerate(sample_questions):
        if cols[i].button(f"✅ {q}", key=f"sample_{i}", help=None, use_container_width=True):
            st.session_state["prefill_query"] = q
            st.rerun()
    # Add custom CSS to make the sample question buttons smaller
    st.markdown('''
    <style>
    .stButton>button {
        font-size: 0.95em !important;
        padding: 0.4em 0.7em !important;
        min-width: 0 !important;
        border-radius: 0.6em !important;
        margin-bottom: 0.2em !important;
    }
    </style>
    ''', unsafe_allow_html=True)

    # --- Document Uploader ---
    st.markdown('<div style="margin-top:2em; font-size:1.15em; color:#fffbe7; font-weight:700;">📄 Upload Complaint/Notes for RTI/FIR Draft</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"], key="pdf_uploader")
    if uploaded_file is not None:
        with st.spinner("Processing your document..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post(
                "http://127.0.0.1:8000/upload_doc",
                files=files
            )
            if response.status_code == 200:
                data = response.json()
                st.markdown('<div class="answer-card">📝 <b>Summary:</b><br><br>' + data.get("summary", "No summary.") + '</div>', unsafe_allow_html=True)
                st.markdown('<div class="answer-card">📄 <b>Draft:</b><br><br>' + data.get("draft", "No draft generated.") + '</div>', unsafe_allow_html=True)
                # --- Download as PDF button ---
                if data.get("draft"):
                    pdf_download = st.button("Download Draft as PDF", key="download_pdf_btn")
                    if pdf_download:
                        pdf_response = requests.post(
                            "http://127.0.0.1:8000/generate_pdf",
                            json={"draft": data["draft"]}
                        )
                        if pdf_response.status_code == 200:
                            st.download_button(
                                label="Click here to download your PDF",
                                data=pdf_response.content,
                                file_name="legal_draft.pdf",
                                mime="application/pdf"
                            )
                        else:
                            st.error("Failed to generate PDF. Please try again.")
            else:
                st.error("Failed to process document. Please try again.")

    if ask_btn:
        if not query.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching your rights..."):
                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={"prompt": query}
                )
                try:
                    result = response.json()
                    # st.write("DEBUG: Backend response:", result)
                    answer = ""
                    if isinstance(result.get("response"), dict):
                        answer = result["response"].get("content", "❌ No response received.")
                    else:
                        answer = result.get("response", "❌ No response received.")
                except Exception as e:
                    st.error(f"Failed to parse backend response as JSON. Raw response: {response.text}\nError: {e}")
                    answer = None
                if answer:
                    st.markdown(f'<div class="chat-bubble-q">🧑‍💼 {query}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="chat-bubble-a">📝 {answer}</div>', unsafe_allow_html=True)
                    # --- TTS Output ---
                    tts = gTTS(answer)
                    tts_fp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                    tts.save(tts_fp.name)
                    audio_bytes = None
                    with open(tts_fp.name, 'rb') as audio_file:
                        audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format='audio/mp3')
                    try:
                        os.unlink(tts_fp.name)
                    except PermissionError:
                        pass
                    # --- Save to session history ---
                    if "qa_history" not in st.session_state:
                        st.session_state["qa_history"] = []
                    st.session_state["qa_history"].insert(0, {"q": query, "a": answer})
                    st.session_state["qa_history"] = st.session_state["qa_history"][:5]

    # --- Query History Section ---
    if "qa_history" in st.session_state and st.session_state["qa_history"]:
        st.markdown('<div style="margin-top:2em;font-size:1.15em;color:#fffbe7;font-weight:700;">🕑 Query History</div>', unsafe_allow_html=True)
        for idx, qa in enumerate(st.session_state["qa_history"]):
            with st.expander(f"Q{idx+1}: {qa['q']}"):
                st.markdown(f'<div class="chat-bubble-q">🧑‍💼 {qa["q"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-bubble-a">📝 {qa["a"]}</div>', unsafe_allow_html=True)
                st.button("Copy Answer", key=f"copy_{idx}", on_click=st.session_state.setdefault("_copy", lambda: None))

st.markdown('''
<div class="footer" style="margin-top:2em;">
  <span style="font-size:1.1em;">Made with <span style="color:#e25555;">❤️</span> by <b>Sheraj</b></span><br>
  <span style="font-size:1.2em;">
    <a href="https://github.com/sherajsharif" target="_blank" style="text-decoration:none;margin:0 10px;">
      <img src="https://img.icons8.com/ios-filled/24/3a8dde/github.png" style="vertical-align:middle;"/> GitHub
    </a> |
    <a href="https://www.linkedin.com/in/sheraj-sharif-652723250/" target="_blank" style="text-decoration:none;margin:0 10px;">
      <img src="https://img.icons8.com/ios-filled/24/3a8dde/linkedin.png" style="vertical-align:middle;"/> LinkedIn
    </a> |
    <a href="https://www.instagram.com/sheraj_sharif" target="_blank" style="text-decoration:none;margin:0 10px;">
      <img src="https://img.icons8.com/ios-filled/24/3a8dde/instagram-new.png" style="vertical-align:middle;"/> Instagram
    </a> |
    <a href="mailto:sherajsharif786@gmail.com" style="text-decoration:none;margin:0 10px;">
      <img src="https://img.icons8.com/ios-filled/24/3a8dde/new-post.png" style="vertical-align:middle;"/> sherajsharif786@gmail.com
    </a>
  </span>
</div>
''', unsafe_allow_html=True)
