import streamlit as st
import google.generativeai as genai
import os, uuid
from pathlib import Path

st.set_page_config(page_title="Indian AI - Real", layout="wide")
GENERATED_DIR = Path("generated")
GENERATED_DIR.mkdir(exist_ok=True)

GEMINI_KEY = st.secrets.get("GEMINI_KEY") or os.getenv("GEMINI_KEY")

if not GEMINI_KEY:
    st.error("Add GEMINI_KEY in Streamlit Secrets. Get from: https://aistudio.google.com/app/apikey")
    st.stop()

genai.configure(api_key=GEMINI_KEY)

def generate_image(prompt):
    real_prompt = prompt + ", photorealistic, ultra realistic, real life photo, DSLR, 8k, highly detailed"
    model = genai.GenerativeModel("gemini-2.5-flash-image")
    response = model.generate_content(real_prompt)
    image_bytes = response.parts[0].inline_data.data
    file_path = GENERATED_DIR / f"image_{uuid.uuid4().hex}.jpg"
    with open(file_path, "wb") as f:
        f.write(image_bytes)
    return str(file_path)

st.title("Indian AI - Real Life Generator (FREE FOREVER)")
st.markdown("500 images/day FREE - No Card - aistudio.google.com")

prompt = st.text_input("Enter prompt", "Chota Bheem as real 8 year old Indian boy, real life")

if st.button("Generate REAL Image"):
    with st.spinner("Generating real life..."):
        try:
            path = generate_image(prompt)
            st.image(path, caption="Real Generation")
            st.success("Done! Saved: " + path)
        except Exception as e:
            st.error(f"Error: {e}")

with st.sidebar:
    st.markdown("FREE FOREVER SETUP:")
    st.markdown("1. Go to: https://aistudio.google.com/app/apikey")
    st.markdown("2. Create API Key (no card)")
    st.markdown("3. In Streamlit: Settings -> Secrets -> Add:")
    st.code('GEMINI_KEY = "your_key_here"')
    st.markdown("4. Save + Reboot")
