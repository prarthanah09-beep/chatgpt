import streamlit as st
import os, uuid, base64, requests, io
from pathlib import Path
from PIL import Image

st.set_page_config(page_title="Indian AI Generator", layout="wide")

def get_bg(path):
    p = Path(path)
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return None

bg_data = get_bg("static/india.jpg")
bg_url = f'url("data:image/jpg;base64,{bg_data}")' if bg_data else 'url("https://images.unsplash.com/photo-1531146020307-15e1d84d0b67?q=80&w=2000")'

st.markdown(f"""
<style>
.stApp {{
    background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.85)), {bg_url};
    background-size: cover;
    background-attachment: fixed;
}}
.black-box {{
    background-color: #000000;
    color: #FFFFFF !important;
    padding: 25px;
    border-radius: 15px;
    border: 2px solid #FFFFFF;
    margin-bottom: 20px;
}}
.black-box * {{ color: #FFFFFF !important; }}
div.stButton > button {{
    background-color: #FFFFFF !important;
    color: #000000 !important;
    font-weight: 900 !important;
    font-size: 18px !important;
    border-radius: 10px !important;
    width: 100%;
}}
section[data-testid="stFileUploader"] {{
    background-color: #000000;
    border: 2px dashed white;
    border-radius: 10px;
    padding: 15px;
}}
section[data-testid="stFileUploader"] * {{ color: white !important; }}
.stTextArea textarea {{
    background: #111111 !important;
    color: white !important;
    border: 2px solid white !important;
    border-radius: 10px !important;
}}
</style>
""", unsafe_allow_html=True)

HF_KEY = st.secrets.get("HF_TOKEN") if hasattr(st, 'secrets') else os.getenv("HF_TOKEN")

st.markdown('<div class="black-box"><h2>🇮🇳 INDIAN AI GENERATOR</h2><p>Black Box | White Text | File + Ask AI</p></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="black-box"><h3>📁 FILE BUTTON</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload", type=["jpg","jpeg","png","webp","pdf","txt"], label_visibility="collapsed")
    if uploaded_file and uploaded_file.type.startswith("image"):
        st.image(uploaded_file, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="black-box"><h3>💬 ASK AI</h3>', unsafe_allow_html=True)
    prompt = st.text_area("Prompt", "Realistic Indian style, photorealistic, 8k, ultra detailed", height=120, label_visibility="collapsed")
    ask_button = st.button("ASK AI - GENERATE")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="black-box"><h3>🎨 AI OUTPUT</h3>', unsafe_allow_html=True)
    if ask_button and prompt:
        if not HF_KEY:
            st.error("Add HF_TOKEN in Secrets")
        else:
            with st.spinner("Generating... 30 sec"):
                # NEW WORKING MODEL
                API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
                headers = {"Authorization": f"Bearer {HF_KEY}"}
                try:
                    r = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=120)
                    if r.status_code == 200:
                        image = Image.open(io.BytesIO(r.content))
                        Path("generated").mkdir(exist_ok=True)
                        save_path = f"generated/{uuid.uuid4().hex}.jpg"
                        image.save(save_path)
                        st.image(save_path, use_container_width=True)
                        st.download_button("📥 DOWNLOAD", open(save_path,"rb"), file_name="ai.jpg", mime="image/jpeg")
                        st.success("Done! FREE Model Working")
                    else:
                        st.error(f"Error: {r.text[:400]}")
                        if "loading" in r.text.lower():
                            st.info("Wait 20 sec and click ASK AI again - model waking up")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("Upload + Prompt + ASK AI")
    st.markdown('</div>', unsafe_allow_html=True)
