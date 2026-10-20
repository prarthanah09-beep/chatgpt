import streamlit as st
import os, uuid, base64, requests, io, time
from pathlib import Path
from PIL import Image

st.set_page_config(page_title="Indian AI Generator", layout="wide")

# Background from static/india.jpg
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
    background-position: center;
    background-attachment: fixed;
}}
/* BLACK BOX WHITE TEXT */
.black-box {{
    background-color: #000000;
    color: #FFFFFF !important;
    padding: 25px;
    border-radius: 15px;
    border: 2px solid #FFFFFF;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(255,255,255,0.2);
}}
.black-box h2, .black-box h3, .black-box p, .black-box label {{
    color: #FFFFFF !important;
}}
.black-box * {{
    color: #FFFFFF !important;
}}

/* Buttons */
div.stButton > button {{
    background-color: #FFFFFF !important;
    color: #000000 !important;
    font-weight: 900 !important;
    font-size: 18px !important;
    border-radius: 10px !important;
    border: 2px solid black !important;
    padding: 12px !important;
    width: 100%;
}}
div.stButton > button:hover {{
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border: 2px solid white !important;
}}

/* File uploader as button */
section[data-testid="stFileUploader"] {{
    background-color: #000000;
    border: 2px dashed white;
    border-radius: 10px;
    padding: 15px;
}}
section[data-testid="stFileUploader"] * {{
    color: white !important;
}}
.stTextArea textarea {{
    background: #111111 !important;
    color: white !important;
    border: 2px solid white !important;
    border-radius: 10px !important;
}}
</style>
""", unsafe_allow_html=True)

HF_KEY = st.secrets.get("HF_TOKEN") if hasattr(st, 'secrets') else os.getenv("HF_TOKEN")
TOGETHER_KEY = st.secrets.get("TOGETHER_API_KEY") if hasattr(st, 'secrets') else os.getenv("TOGETHER_API_KEY")

# --- UI ---
st.markdown('<div class="black-box"><h2>🇮🇳 INDIAN AI GENERATOR</h2><p>Black Box Design | White Text | File Upload | Ask AI</p></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="black-box">', unsafe_allow_html=True)
    st.markdown("### 📁 FILE BUTTON")
    uploaded_file = st.file_uploader("Upload Image / File", type=["jpg","jpeg","png","webp","pdf","txt"], label_visibility="collapsed")
    if uploaded_file:
        if uploaded_file.type.startswith("image"):
            st.image(uploaded_file, caption="Uploaded File", use_container_width=True)
        else:
            st.success(f"File uploaded: {uploaded_file.name}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="black-box">', unsafe_allow_html=True)
    st.markdown("### 💬 ASK AI")
    prompt = st.text_area("Ask anything...", "Make this image realistic Indian style, photorealistic, 8k", height=120, label_visibility="collapsed")
    ask_button = st.button("ASK AI - GENERATE")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="black-box">', unsafe_allow_html=True)
    st.markdown("### 🎨 AI OUTPUT")
    
    if ask_button and prompt:
        if not HF_KEY and not TOGETHER_KEY:
            st.error("Add HF_TOKEN in Secrets")
            st.code('HF_TOKEN = "hf_..."', language="bash")
        else:
            with st.spinner("AI Thinking..."):
                try:
                    if HF_KEY:
                        API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
                        headers = {"Authorization": f"Bearer {HF_KEY}"}
                        final_prompt = f"{prompt}, photorealistic, ultra realistic Indian, real skin, DSLR, 8k"
                        r = requests.post(API_URL, headers=headers, json={"inputs": final_prompt}, timeout=90)
                        if r.status_code == 200:
                            image = Image.open(io.BytesIO(r.content))
                            Path("generated").mkdir(exist_ok=True)
                            save_path = f"generated/{uuid.uuid4().hex}.jpg"
                            image.save(save_path)
                            st.image(save_path, caption="AI Generated", use_container_width=True)
                            st.download_button("📥 DOWNLOAD IMAGE", open(save_path,"rb"), file_name="indian_ai.jpg", mime="image/jpeg", key="dl1")
                            st.success("✅ Generated with FREE HF")
                        elif "loading" in r.text.lower():
                            st.warning("Model loading, wait 20 sec and click ASK AI again")
                        else:
                            st.error(f"HF Error: {r.text[:300]}")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("Upload file + Write prompt + Click ASK AI")
        if bg_data:
            st.success("✅ Background: static/india.jpg is active")

    st.markdown('</div>', unsafe_allow_html=True)
