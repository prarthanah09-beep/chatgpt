import streamlit as st, urllib.parse, random, base64
from pathlib import Path

st.set_page_config(page_title="ChatGPT", layout="wide")

def get_bg():
    p = Path("static/india.jpg")
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return None

bg = get_bg()
if bg:
    st.markdown(f"""<style>.stApp{{background:linear-gradient(rgba(0,0,0,0.75),rgba(0,0,0,0.85)),url("data:image/jpg;base64,{bg}");background-size:cover;background-position:center}}</style>""", unsafe_allow_html=True)
else:
    st.markdown("<style>.stApp{background:#000!important}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.center{color:white;font-size:28px;text-align:center;margin-top:20vh;margin-bottom:25px}
/* FIX: ONLY 1 + - HIDE ALL ICONS */
div[data-testid="stFileUploader"]{background:transparent!important;border:none!important}
div[data-testid="stFileUploader"] section{background:#000!important;border:1px solid #333!important;border-radius:12px!important;min-height:52px!important;padding:0!important;display:flex!important;align-items:center!important;justify-content:center!important}
div[data-testid="stFileUploader"] section > div, div[data-testid="stFileUploader"] section svg, div[data-testid="stFileUploader"] section span, div[data-testid="stFileUploader"] section small{display:none!important}
div[data-testid="stFileUploader"] section button{background:#000!important;color:white!important;border:1px solid #555!important;border-radius:12px!important;width:60px!important;height:52px!important}
div[data-testid="stFileUploader"] section button *{display:none!important}
div[data-testid="stFileUploader"] section button::after{content:"+";color:white;font-size:32px;font-weight:300;display:block!important}
/* ASK CHAT - BLACK BOX WHITE TEXT */
.stTextInput input{background:#000!important;color:white!important;border:1px solid #333!important;border-radius:12px!important;height:52px!important}
.stTextInput input::placeholder{color:white!important}
div.stButton>button{background:white!important;color:black!important;border-radius:25px!important;width:100%;height:50px;font-weight:700!important}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

_, mid, _ = st.columns([1,2,1])
with mid:
    c1, c2 = st.columns([1,4])
    with c1:
        st.file_uploader("", type=["jpg","png","webp"], label_visibility="collapsed")
    with c2:
        prompt = st.text_input("", placeholder="Ask ChatGPT", label_visibility="collapsed")
    
    if st.button("Generate"):
        if prompt:
            enc = urllib.parse.quote(prompt + ", photorealistic, 8k")
            seed = random.randint(1, 9999999)
            url = f"https://image.pollinations.ai/prompt/{enc}?model=flux-realism&width=1024&height=1024&seed={seed}&nologo=true"
            st.image(url, use_container_width=True)
