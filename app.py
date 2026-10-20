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
    background-image: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.85)), {bg_url};
    background-size: cover;
    background-attachment: fixed;
}}
h1, p, label {{ color: white !important; }}
div.stButton > button {{
    background: linear-gradient(90deg, #FF9933, #FFFFFF, #138808);
    color: black !important; font-weight: 900 !important; font-size: 20px !important;
    border-radius: 30px !important; width: 100%; padding: 15px !important;
}}
</style>
""", unsafe_allow_html=True)

HF_KEY = st.secrets.get("HF_TOKEN") if hasattr(st, 'secrets') else None
if not HF_KEY:
    HF_KEY = os.getenv("HF_TOKEN")

if not HF_KEY:
    st.warning("Add HF_TOKEN: Manage app -> Settings -> Secrets -> HF_TOKEN = 'hf_...'")
    st.info("Get free token from huggingface.co/settings/tokens")
    st.stop()

c1, c2 = st.columns([1.2, 1])
with c1:
    st.markdown("# Indian AI Generator")
    prompt = st.text_area("Prompt", "Chota Bheem as real 8 year old Indian boy, school uniform, smiling, photorealistic", height=140)
    btn = st.button("Generate REAL Image - FREE")

with c2:
    if btn:
        with st.spinner("Generating..."):
            API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
            headers = {"Authorization": f"Bearer {HF_KEY}"}
            r = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=120)
            if r.status_code == 200:
                img = Image.open(io.BytesIO(r.content))
                Path("generated").mkdir(exist_ok=True)
                p = f"generated/{uuid.uuid4().hex}.jpg"
                img.save(p)
                st.image(p, use_container_width=True)
                st.download_button("Download", open(p,"rb"), file_name="indian.jpg")
                st.success("Done!")
            else:
                st.error(f"Error: {r.text[:400]}")
                st.info("If 'loading' -> wait 30 sec and try again")
