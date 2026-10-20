import streamlit as st
import google.generativeai as genai
from PIL import Image
import io, os, uuid
from pathlib import Path

# --- CONFIG ---
st.set_page_config(page_title="Indian AI - Real Generation", layout="wide")
GENERATED_DIR = Path("generated")
GENERATED_DIR.mkdir(exist_ok=True)

# --- GET KEY FROM SECRETS ---
# In Streamlit Cloud: Manage app -> Settings -> Secrets -> Add GEMINI_KEY
GEMINI_KEY = st.secrets.get("GEMINI_KEY") or os.getenv("GEMINI_KEY")

if not GEMINI_KEY:
    st.error("Add GEMINI_KEY in Streamlit Secrets. Get free from: https://aistudio.google.com/app/apikey")
    st.stop()

genai.configure(api_key=GEMINI_KEY)

def generate_image(prompt):
    # Make it REAL - no cartoon
    real_prompt = f"{prompt}, photorealistic, ultra realistic, real life photo, DSLR, 8k, highly detailed, real skin, real fur, real human boy, natural lighting"
    
    model = genai.GenerativeModel("gemini-2.5-flash-image")
    
    response = model.generate_content(real_prompt)
    
    # Extract image bytes
    image_bytes = response.parts[0].inline_data.data
    
    # Save
    file_path = GENERATED_DIR / f"image_{uuid.uuid4().hex}.jpg"
    with open(file_path, "wb") as f:
        f.write(image_bytes)
    
    return str(file_path)

# --- UI ---
st.title("🇮🇳 Indian AI - Real Life Generator (FREE FOREVER)")
st.markdown("500 images/day FREE - No Card - aistudio.google.com")

prompt = st.text_input("Enter prompt", "Chota Bheem as real 8 year old Indian boy, real life")

if st.button("Generate REAL Image"):
    with st.spinner("Generating real life..."):
        try:
            path = generate_image(prompt)
            st.image(path, caption="Real Generation", use_column_width=True)
            st.success("Done! Saved: " + path)
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("If limit, wait 1 min or check key at https://aistudio.google.com/app/apikey")

st.sidebar.markdown("""
**FREE FOREVER SETUP:**
1. Go to: **https://aistudio.google.com/app/apikey**
2. Create API Key (no card)
3. In Streamlit: Settings -> Secrets -> Add:
