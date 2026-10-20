import streamlit as st, urllib.parse, random, base64, time, requests
from pathlib import Path

st.set_page_config(page_title="ChatGPT", layout="wide", initial_sidebar_state="collapsed")

API_BASE = st.secrets.get("POLLINATION_API", "https://image.pollinations.ai/prompt")
MODEL = st.secrets.get("MODEL", "flux")

def get_bg():
    p = Path("static/india.jpg")
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return None
bg = get_bg()
if bg:
    st.markdown(f"""<style>.stApp{{background:linear-gradient(rgba(0,0,0,0.6),rgba(0,0,0,0.8)),url("data:image/jpg;base64,{bg}");background-size:cover}}</style>""", unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.center{color:white;font-size:28px;text-align:center;margin-top:18vh;margin-bottom:25px;font-weight:600}

/* ONLY ONE + BOX */
.plus-box{
    background:#000 !important;
    border:1px solid #555 !important;
    border-radius:12px !important;
    height:52px !important;
    width:100% !important;
    color:white !important;
    font-size:32px !important;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
}

/* INVISIBLE FILE INPUT ON TOP OF + - SO MOBILE TAP OPENS GALLERY */
div[data-testid="stFileUploader"]{
    opacity:0 !important;
    position:absolute !important;
    top:0 !important;
    left:0 !important;
    width:100% !important;
    height:52px !important;
    z-index:10 !important;
}
div[data-testid="stFileUploader"] *{opacity:0 !important}

/* BLACK BOXES WHITE TEXT */
div[data-testid="stTextInput"] input{background:#000 !important;color:white !important;border:1px solid #555 !important;border-radius:12px !important;height:52px !important}
div[data-testid="stFormSubmitButton"] button, div[data-testid="stDownloadButton"] button{background:#000 !important;color:white !important;border:1px solid #555 !important;border-radius:12px !important}
div[data-testid="stFormSubmitButton"] button *, div[data-testid="stDownloadButton"] button *{color:white !important}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

if "gen_url" not in st.session_state:
    st.session_state.gen_url=None; st.session_state.gen_data=None; st.session_state.last_gen=0

_, mid, _ = st.columns([1,2,1])
with mid:
    with st.form("chat_form"):
        c1,c2=st.columns([1,4])
        with c1:
            # ONLY ONE + - SINGLE ELEMENT
            st.markdown('<div style="position:relative"><div class="plus-box">+</div>', unsafe_allow_html=True)
            st.file_uploader("file", type=["jpg","png","webp","jpeg"], label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            prompt=st.text_input("prompt", placeholder="Ask ChatGPT", label_visibility="collapsed")
        gen=st.form_submit_button("Generate")

    if gen and prompt:
        now=time.time()
        if now-st.session_state.last_gen<46:
            st.error(f"Wait {int(46-(now-st.session_state.last_gen))} sec")
        else:
            st.session_state.last_gen=now
            url=f"{API_BASE}/{urllib.parse.quote(prompt)}?model={MODEL}&width=1024&height=1024&seed={random.randint(1,9999999)}&nologo=true"
            st.session_state.gen_url=url
            try:
                st.session_state.gen_data=requests.get(url, timeout=30).content
            except:
                st.session_state.gen_data=None
            st.rerun()

    if st.session_state.gen_url:
        st.image(st.session_state.gen_url, use_container_width=True)
        if st.session_state.gen_data:
            b1,b2=st.columns(2)
            with b1:
                st.markdown(f"""<button onclick="navigator.clipboard.writeText('{st.session_state.gen_url}')" style="width:100%;height:48px;background:#000;color:white;border:1px solid #555;border-radius:12px">📋 Copy</button>""", unsafe_allow_html=True)
            with b2:
                st.download_button("⬇️ Download", data=st.session_state.gen_data, file_name="img.jpg", mime="image/jpeg", use_container_width=True)
