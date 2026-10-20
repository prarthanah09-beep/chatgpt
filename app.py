import streamlit as st
import os, uuid, base64, requests
from pathlib import Path

# --- CONFIG ---
st.set_page_config(page_title="Indian AI - Together AI", page_icon="🇮🇳", layout="wide")
GENERATED_DIR = Path("generated")
GENERATED_DIR.mkdir(exist_ok=True)

# --- BACKGROUND FROM static/india.jpg ---
def get_base64_image(image_path):
    if Path(image_path).exists():
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

local_bg = get_base64_image("static/india.jpg")
if local_bg:
    bg_css = f'url("data:image/jpg;base64,{local_bg}")'
else:
    bg_css = 'url("https://images.unsplash.com/photo-1531146020307-15e1d84d0b67?q=80&w=2000")'

st.markdown(f"""
<style>
.stApp {{
    background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.85)), {bg_css};
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
h1, h2, h3, p, label {{ color: white !important; }}
.stTextArea textarea {{ background: rgba(255,255,255,0.95) !important; color: black !important; border-radius: 15px !important; font-size: 17px !important; }}
div.stButton > button {{
    background: linear-gradient(90deg, #FF9933, #FFFFFF, #138808);
    color: black !important; font-weight: 900 !important; font-size: 20px !important;
    border-radius: 30px !important; padding: 15px !important; width: 100%; border: none !important;
}}
.image-card {{ background: rgba(255,255,255,0.12); backdrop-filter: blur(12px); border-radius: 20px; padding: 25px; border: 1px solid rgba(255,255,255,0.2); }}
</style>
""", unsafe_allow_html=True)

# --- TOGETHER AI KEY ---
TOGETHER_KEY = st.secrets.get("TOGETHER_API_KEY") if hasattr(st, 'secrets') else None
if not TOGETHER_KEY:
    TOGETHER_KEY = os.getenv("TOGETHER_API_KEY") or os.getenv("TOGETHER_KEY")

if not TOGETHER_KEY:
    st.error("❌ Together AI Key Missing")
    st.info("Get FREE key from: https://api.together.xyz/settings/api-keys\nThen in Streamlit: Manage app -> Settings -> Secrets -> Add:\nTOGETHER_API_KEY = 'your_key_here'")
    st.stop()

# --- GENERATOR ---
def generate_with_together(prompt):
    # Best models on Together AI
    real_prompt = f"{prompt}, photorealistic, ultra realistic Indian person, real life photo, natural skin texture, DSLR, 8k, highly detailed, India"
    
    url = "https://api.together.xyz/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {TOGETHER_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "black-forest-labs/FLUX.1-schnell-Free",  # FREE model, super fast
        "prompt": real_prompt,
        "width": 1024,
        "height": 1024,
        "steps": 4,
        "n": 1
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        # Try fallback model if free model fails
        payload["model"] = "black-forest-labs/FLUX.1-dev"
        response = requests.post(url, json=payload, headers=headers)
    
    response.raise_for_status()
    data = response.json()
    
    # Get image URL and download
    image_url = data['data'][0]['url']
    img_data = requests.get(image_url).content
    
    file_path = GENERATED_DIR / f"img_{uuid.uuid4().hex}.jpg"
    with open(file_path, "wb") as f:
        f.write(img_data)
    
    return str(file_path)

# --- UI ---
c1, c2 = st.columns([1.2, 1])

with c1:
    st.markdown("# 🇮🇳 Indian AI - Together AI Generator")
    st.markdown("### FLUX Model | Free & Fast")
    st.markdown('<div class="image-card">', unsafe_allow_html=True)
    prompt = st.text_area("Prompt", "Chota Bheem as real 8 year old Indian boy, real life, school uniform, smiling, ultra realistic", height=130)
    btn = st.button("✨ Generate REAL Image")
    st.caption("Free models: FLUX Schnell (fast), FLUX Dev (quality)")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    if btn and prompt:
        with st.spinner("Generating with Together AI... 5 sec"):
            try:
                path = generate_with_together(prompt)
                st.markdown('<div class="image-card">', unsafe_allow_html=True)
                st.image(path, caption="Generated with Together AI - FLUX", use_container_width=True)
                with open(path, "rb") as f:
                    st.download_button("📥 Download HD", f, file_name="indian_real.jpg", mime="image/jpeg")
                st.success("Done!")
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("If 401: Your Together key is wrong. If 429: Wait 10 sec. Get new free key at together.ai")
    else:
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        st.info("👈 Your REAL image will appear here")
        if local_bg:
            st.success("✅ Using static/india.jpg")
        else:
            st.warning("⚠️ Put your image in static/india.jpg in GitHub repo")
        st.markdown('</div>', unsafe_allow_html=True)
