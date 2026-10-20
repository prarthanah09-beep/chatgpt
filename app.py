import streamlit as st
import urllib.parse, random, base64
from pathlib import Path

st.set_page_config(page_title="ChatGPT", layout="wide")

# static/india.jpg background with black overlay
def get_bg():
    p = Path("static/india.jpg")
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return None

bg = get_bg()
if bg:
    st.markdown(f"""
    <style>
    .stApp{{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), url("data:image/jpg;base64,{bg}");
        background-size: cover; background-position: center;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("<style>.stApp{background:#000!important}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.block-container{padding:0!important}
.top{display:flex;justify-content:space-between;align-items:center;padding:10px 16px}
.hamburger{background:#1a1a1a;border-radius:50%;width:42px;height:42px;display:flex;align-items:center;justify-content:center;color:white}
.upgrade{background:#1e1e1e;border-radius:24px;padding:10px 18px;color:#a78bfa;font-weight:600;border:1px solid #333;display:flex;align-items:center;gap:6px}
.profile{background:#1a1a1a;border-radius:24px;padding:6px 12px;display:flex;gap:12px}
.center-text{color:white;font-size:28px;font-weight:500;text-align:center;margin-top:30vh}
.bottom{position:fixed;bottom:90px;left:12px;right:12px;display:flex;gap:10px;align-items:center}
.plus{background:#212121;border-radius:50%;min-width:52px;height:52px;display:flex;align-items:center;justify-content:center;color:white;font-size:30px;border:1px solid #333}
.ask{background:#2f2f2f;border-radius:28px;flex:1;height:52px;display:flex;align-items:center;padding:0 16px;border:1px solid #444;color:#888}
.keyboard{position:fixed;bottom:0;left:0;right:0;background:#1c1c1e;padding:8px}
div.stButton>button{background:white!important;color:black!important;border-radius:25px!important;width:100%;height:50px;font-weight:800!important}
</style>
""", unsafe_allow_html=True)

# TOP BAR - EXACT LIKE SCREENSHOT
st.markdown("""
<div class="top">
    <div style="display:flex;gap:10px;align-items:center">
        <div class="hamburger">☰</div>
        <div class="upgrade">◆ Upgrade</div>
    </div>
    <div class="profile">
        <span style="font-size:22px;color:white">👤+</span>
        <span style="font-size:22px;color:white">◍</span>
    </div>
</div>
""", unsafe_allow_html=True)

# CENTER - EXACT LIKE SCREENSHOT
st.markdown('<div class="center-text">What can I help with?</div>', unsafe_allow_html=True)

# BOTTOM INPUT AREA - EXACT LIKE SCREENSHOT
_, mid, _ = st.columns([1,2,1])
with mid:
    # File + Ask ChatGPT bar like screenshot
    c1, c2 = st.columns([1,5])
    with c1:
        uploaded = st.file_uploader("+", type=["jpg","png","webp"], label_visibility="collapsed")
        st.markdown('<div style="text-align:center;color:white;font-size:30px;margin-top:-38px;pointer-events:none">+</div>', unsafe_allow_html=True)
    with c2:
        prompt = st.text_input("Ask", placeholder="Ask ChatGPT", label_visibility="collapsed")
    
    if uploaded:
        st.image(uploaded, use_container_width=True)
    
    if st.button("Generate", use_container_width=True) and prompt:
        # REAL MODEL - WORKING
        real_prompt = prompt + ", photorealistic, ultra realistic, real skin, 8k"
        enc = urllib.parse.quote(real_prompt)
        seed = random.randint(1, 9999999)
        url = f"https://image.pollinations.ai/prompt/{enc}?model=flux-realism&width=1024&height=1024&seed={seed}&nologo=true&enhance=true"
        st.image(url, caption=f"REAL - flux-realism - {seed}", use_container_width=True)
        st.success("✅ Generated - REAL Model")
        st.markdown(f"[HD Link]({url})")
    
    if not bg:
        st.warning("Add static/india.jpg in GitHub > static folder")
    else:
        st.success("✅ static/india.jpg background active")
