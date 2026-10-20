import streamlit as st
from google import genai
import os, uuid, base64
from pathlib import Path

# --- CONFIG ---
st.set_page_config(page_title="Indian AI - Real Generator", page_icon="🇮🇳", layout="wide")
GENERATED_DIR = Path("generated")
GENERATED_DIR.mkdir(exist_ok=True)

# --- BACKGROUND FROM static/india.jpg ---
def get_base64_image(image_path):
    if Path(image_path).exists():
        with open(image_path, "rb") as img:
            return base64.b64encode(img.read()).decode()
    return None

# Try local file first, then fallback
local_bg = get_base64_image("static/india.jpg")
if local_bg:
    bg_css = f'url("data:image/jpg;base64,{local_bg}")'
else:
    # Fallback if static not found
    bg_css = 'url("https://images.unsplash.com/photo-1531146020307-15e1d84d0b67?q=80&w=2000")'

st.markdown(f"""
<style>
.stApp {{
    background-image: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.85)), {bg_css};
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
h1, h2, h3, p, label {{ color: white !important; }}
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
    padding: 15px !important;
    border: none !important;
    width: 100%;
    box-shadow: 0 4px 15px rgba(255,153,51,0.4);
}}
div.stButton > button:hover {{
    transform: scale(1.02);
    box-shadow: 0 0 30px #FF9933;
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

# --- API KEY - Works on BOTH Streamlit + Hugging Face ---
GEMINI_KEY = st.secrets.get("GEMINI_KEY") if hasattr(st, 'secrets') else None
if not GEMINI_KEY:
    GEMINI_KEY = os.getenv("GEMINI_KEY") or os.getenv("GOOGLE_API_KEY")

if not GEMINI_KEY:
    st.error("❌ API Key Missing")
    st.info("Streamlit Cloud: Manage app -> Settings -> Secrets -> GEMINI_KEY\nHugging Face: Space Settings -> Variables and Secrets -> New Secret")
    st.stop()

client = genai.Client(api_key=GEMINI_KEY)

# --- GENERATOR WITH 3 MODEL FALLBACK (NO 429) ---
def generate_image(prompt):
    real_prompt = f"{prompt}, photorealistic, ultra realistic, real life photo, Indian person, natural skin texture, DSLR, 8k, highly detailed"
    models_to_try = [
        "gemini-2.5-flash-image",
        "gemini-2.0-flash-preview-image-generation",
        "gemini-2.0-flash-exp-image-generation"
    ]
    last_err = ""
    for m in models_to_try:
        try:
            response = client.models.generate_content(model=m, contents=[real_prompt])
            for part in response.parts:
                if part.inline_data:
                    file_path = GENERATED_DIR / f"img_{uuid.uuid4().hex}.jpg"
                    with open(file_path, "wb") as f:
                        f.write(part.inline_data.data)
                    return str(file_path), m
        except Exception as e:
            last_err = str(e)
            continue
    raise Exception(last_err)

# --- UI ---
c1, c2 = st.columns([1.2, 1])

with c1:
    st.markdown("# 🇮🇳 Indian AI - Real Life Generator")
    st.markdown("### 1000 Images/Day FREE | No Credit Card")
    st.markdown('<div class="image-card">', unsafe_allow_html=True)
    prompt = st.text_area("Prompt", "Chota Bheem as real 8 year old Indian boy, real life, school uniform, smiling, ultra realistic", height=130)
    btn = st.button("✨ Generate REAL Image")
    st.caption("Try: Motu Patlu real, Shinchan as Indian boy, Doraemon real cat, Little Singham real")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    if btn and prompt:
        with st.spinner("Creating real photo... 10 sec"):
            try:
                path, model_used = generate_image(prompt)
                st.markdown('<div class="image-card">', unsafe_allow_html=True)
                st.image(path, caption=f"Made with {model_used}", use_container_width=True)
                with open(path, "rb") as f:
                    st.download_button("📥 Download HD", f, file_name="indian_real.jpg", mime="image/jpeg")
                st.success(f"Generated!")
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                if "429" in str(e):
                    st.error("⏳ Free limit: Wait 60 seconds and try again")
                else:
                    st.error(f"Error: {e}")
    else:
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        st.info("👈 Your REAL image will appear here")
        if local_bg:
            st.success("✅ Using your static/india.jpg as background")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<center style='color:rgba(255,255,255,0.7);margin-top:40px;'>Made with ❤️ in India | Works on Streamlit + Hugging Face</center>", unsafe_allow_html=True)
