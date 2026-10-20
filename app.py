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
    st.error("Add HF_TOKEN in Secrets: huggingface.co/settings/tokens")
    st.stop()

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("# Indian AI Generator")
    prompt = st.text_area("Prompt", "Chota Bheem as real 8 year old Indian boy, school uniform, smiling, photorealistic, ultra realistic", height=140)
    btn = st.button("Generate REAL Image - FREE")

with col2:
    if btn:
        with st.spinner("Generating FREE... 20 sec"):
            try:
                API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
                headers = {"Authorization": f"Bearer {HF_KEY}"}
                payload = {"inputs": f"{prompt}, photorealistic, ultra realistic, real Indian person, DSLR, 8k"}
                
                response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
                
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    Path("generated").mkdir(exist_ok=True)
                    path = f"generated/{uuid.uuid4().hex}.jpg"
                    image.save(path)
                    st.image(path, use_container_width=True)
                    st.download_button("Download HD", open(path,"rb"), file_name="indian.jpg", mime="image/jpeg")
                    st.success("Done! FREE")
                else:
                    st.error(f"Error {response.status_code}: {response.text[:300]}")
                    if "loading" in response.text.lower():
                        st.info("Model is loading - wait 30 sec and click again (free model sleeps)")
            except Exception as e:
                st.error(f"Error: {e}")
