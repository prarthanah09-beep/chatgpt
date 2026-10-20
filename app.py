import streamlit as st
import os, uuid, base64
from pathlib import Path
from huggingface_hub import InferenceClient

# No page icon
st.set_page_config(page_title="Indian AI Generator", layout="wide")

# Background from static/india.jpg
def get_bg(path):
    p = Path(path)
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return None

bg_data = get_bg("static/india.jpg")
if bg_data:
    bg_url = f'url("data:image/jpg;base64,{bg_data}")'
else:
    bg_url = 'url("https://images.unsplash.com/photo-1531146020307-15e1d84d0b67?q=80&w=2000")'

st.markdown(f"""
<style>
.stApp {{
    background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.85)), {bg_url};
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
h1, p, label {{ color: white !important; }}
.stTextArea textarea {{
    background: rgba(255,255,255,0.95) !important;
    color: black !important;
    border-radius: 15px !important;
    font-size: 17px !important;
}}
div.stButton > button {{
    background: linear-gradient(90deg, #FF9933, #FFFFFF, #138808);
    color: black !important;
    font-weight: 900 !important;
    font-size: 20px !important;
    border-radius: 30px !important;
    width: 100%;
    padding: 15px !important;
}}
.image-card {{
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.2);
}}
</style>
""", unsafe_allow_html=True)

HF_KEY = st.secrets.get("HF_TOKEN") if hasattr(st, 'secrets') else None
if not HF_KEY:
    HF_KEY = os.getenv("HF_TOKEN")

if not HF_KEY:
    st.error("Add HF_TOKEN in Secrets")
    st.stop()

client = InferenceClient(api_key=HF_KEY)

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("# Indian AI Generator")
    st.markdown("FLUX Model - FREE - No $15 needed")
    st.markdown('<div class="image-card">', unsafe_allow_html=True)
    prompt = st.text_area("Enter prompt", "Chota Bheem as real 8 year old Indian boy, school uniform, smiling, photorealistic, ultra realistic, natural skin texture, real life", height=140)
    generate = st.button("Generate REAL Image")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if generate and prompt:
        with st.spinner("Generating... 15 sec (FREE)"):
            try:
                final_prompt = f"{prompt}, photorealistic, ultra realistic, real Indian person, natural skin, DSLR photo, 8k, highly detailed"
                image = client.text_to_image(final_prompt, model="black-forest-labs/FLUX.1-schnell")
                
                Path("generated").mkdir(exist_ok=True)
                save_path = f"generated/{uuid.uuid4().hex}.jpg"
                image.save(save_path)
                
                st.markdown('<div class="image-card">', unsafe_allow_html=True)
                st.image(save_path, caption="Generated - FREE FLUX", use_container_width=True)
                st.download_button("Download HD", open(save_path,"rb"), file_name="indian_real.jpg", mime="image/jpeg")
                st.success("Done! FREE")
                st.markdown('</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Error: {e}")
                if "429" in str(e):
                    st.info("Free server busy - wait 30 sec, try again.")
    else:
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        st.info("Your image will appear here")
        if bg_data:
            st.success("Using static/india.jpg background")
        else:
            st.warning("Add your image as static/india.jpg in GitHub repo")
        st.markdown('</div>', unsafe_allow_html=True)
