import streamlit as st
import requests, io, uuid, random, urllib.parse
from pathlib import Path
from PIL import Image

st.set_page_config(page_title="ChatGPT", layout="wide", page_icon=None)

st.markdown("""
<style>
.stApp { background: #000000 !important; }
header, footer {visibility: hidden;}
.block-container { padding-top: 0px !important; }

/* Top bar like your screenshot */
.top-bar {
    display: flex; justify-content: space-between; align-items: center;
    padding: 12px 10px; background: #000; position: sticky; top: 0; z-index: 99;
}
.icon-btn { background: #1a1a1a; border-radius: 50%; padding: 10px 12px; color: white; }
.upgrade-btn {
    background: #2a2a2a; color: #9ca3ff; padding: 8px 18px;
    border-radius: 20px; font-weight: 600; border: none; font-size: 15px;
}
.center-text {
    color: white; font-size: 34px; font-weight: 500;
    text-align: center; margin-top: 180px; margin-bottom: 100px;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}
.chat-bar {
    background: #2f2f2f; border-radius: 28px; padding: 12px 16px;
    display: flex; align-items: center; gap: 12px;
    max-width: 800px; margin: 0 auto; border: 1px solid #444;
}
.file-plus {
    background: #212121; border-radius: 50%; width: 36px; height: 36px;
    display: flex; align-items: center; justify-content: center; color: white; font-size: 22px;
}
.input-field input { background: transparent !important; color: white !important; border: none !important; }
div.stButton > button {
    background: white !important; color: black !important;
    border-radius: 20px !important; font-weight: 700 !important; height: 48px;
}
.black-card { background: #111; border: 1px solid #333; border-radius: 16px; padding: 20px; margin: 15px 0; }
.black-card * { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- TOP BAR LIKE SCREENSHOT ---
st.markdown("""
<div class="top-bar">
    <div style="display:flex; gap:12px; align-items:center;">
        <div class="icon-btn">☰</div>
        <div class="upgrade-btn">✦ Upgrade</div>
    </div>
    <div style="display:flex; gap:10px;">
        <div class="icon-btn">👤+</div>
        <div class="icon-btn">◍</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- CENTER TEXT LIKE SCREENSHOT ---
st.markdown('<div class="center-text">What can I help with?</div>', unsafe_allow_html=True)

# --- MAIN CHATGPT STYLE INPUT ---
col_left, col_center, col_right = st.columns([1, 2.2, 1])

with col_center:
    # REAL MODEL SELECTOR - HIDDEN, DEFAULT REAL
    real_model = "flux-realism"  # REAL MODEL - photorealistic
    
    st.markdown('<div class="black-card">', unsafe_allow_html=True)
    st.markdown(f"**REAL MODEL:** `{real_model}` - Ultra Realistic Indian Photos")
    
    # File button like + in your screenshot
    uploaded = st.file_uploader("📎 Upload file (like + button in your screenshot)", 
                                 type=["jpg","jpeg","png","webp"], label_visibility="visible")
    if uploaded:
        st.image(uploaded, caption="Uploaded", use_container_width=True)
    
    # Ask ChatGPT input like your screenshot
    prompt = st.text_area("Ask ChatGPT", 
                          placeholder="Ask ChatGPT",
                          value="Real Indian woman in beautiful saree, futuristic AI background, photorealistic, ultra realistic skin texture, natural, 8k, DSLR photo",
                          height=110, label_visibility="collapsed")
    
    generate = st.button("Ask ChatGPT - Generate REAL Image", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- GENERATE WITH REAL MODEL ---
    if generate and prompt:
        with st.spinner(f"Generating REAL image with {real_model}... 10 sec"):
            try:
                # REAL MODEL PROMPT - Make it ultra realistic
                real_prompt = f"{prompt}, photorealistic, ultra realistic, real human skin, natural texture, Indian, highly detailed, 8k, professional photography, sharp focus, real life"
                encoded = urllib.parse.quote(real_prompt)
                seed = random.randint(1, 9999999)
                
                # POLLINATION REAL MODEL - FREE
                url = f"https://image.pollinations.ai/prompt/{encoded}?model={real_model}&width=1024&height=1024&seed={seed}&nologo=true&enhance=true&safe=false"
                
                r = requests.get(url, timeout=90)
                if r.status_code == 200:
                    img = Image.open(io.BytesIO(r.content))
                    Path("generated").mkdir(exist_ok=True)
                    save_path = f"generated/{uuid.uuid4().hex}.jpg"
                    img.save(save_path)
                    
                    st.markdown('<div class="black-card">', unsafe_allow_html=True)
                    st.image(save_path, caption=f"REAL MODEL: {real_model}", use_container_width=True)
                    st.download_button("📥 DOWNLOAD REAL IMAGE", 
                                       open(save_path,"rb"), 
                                       file_name="real_indian_ai.jpg", 
                                       mime="image/jpeg", use_container_width=True)
                    st.success(f"✅ REAL image generated with {real_model}")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error(f"Error {r.status_code}, retry")
            except Exception as e:
                st.error(f"Error: {e} - Try again")
    
    # Bottom bar like ChatGPT keyboard area
    st.markdown("""
    <div style="margin-top:80px; text-align:center; color:#666; font-size:13px;">
        Pollination AI • Real Model: flux-realism • FREE • No Token<br>
        Your file from static/india.jpg is used as background
    </div>
    """, unsafe_allow_html=True)
