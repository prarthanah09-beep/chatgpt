import streamlit as st, urllib.parse, random, base64
from pathlib import Path

st.set_page_config(page_title="ChatGPT", layout="wide")

# Background image - NO MESSAGE
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
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.8)), url("data:image/jpg;base64,{bg}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("<style>.stApp{background:#000!important}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.block-container{padding-top:20px!important}
.center{color:white;font-size:28px;font-weight:500;text-align:center;margin-top:25vh;margin-bottom:30px}
div[data-testid="stFileUploader"]{background:#000!important;border:1px solid #333!important;border-radius:12px!important}
div[data-testid="stFileUploader"] *{color:white!important}
div[data-testid="stFileUploader"] button{background:#000!important;color:white!important;border:1px solid #555!important}
div[data-testid="stFileUploader"] small{display:none!important}
.stTextInput input{background:#2f2f2f!important;color:white!important;border-radius:12px!important;border:1px solid #444!important;height:52px}
div.stButton>button{background:white!important;color:black!important;border-radius:25px!important;width:100%;height:50px;font-weight:700!important}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

_, mid, _ = st.columns([1,2,1])
with mid:
    # ONLY + AND ASK - NOTHING ELSE
    c1, c2 = st.columns([1,4])
    with c1:
        uploaded = st.file_uploader("", type=["jpg","png","webp"], label_visibility="collapsed")
    with c2:
        prompt = st.text_input("", placeholder="Ask ChatGPT", label_visibility="collapsed")
    
    if st.button("Generate"):
        if prompt:
            enc = urllib.parse.quote(prompt + ", photorealistic, ultra realistic, 8k")
            seed = random.randint(1, 9999999)
            url = f"https://image.pollinations.ai/prompt/{enc}?model=flux-realism&width=1024&height=1024&seed={seed}&nologo=true&enhance=true"
            st.image(url, use_container_width=True)
