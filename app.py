import streamlit as st, urllib.parse, random, base64, time, requests
from pathlib import Path

st.set_page_config(page_title="ChatGPT", layout="wide")

API_BASE = st.secrets.get("POLLINATION_API", "https://image.pollinations.ai/prompt")
MODEL = st.secrets.get("MODEL", "flux")

def get_bg():
    p = Path("static/india.jpg")
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return None

bg = get_bg()
if bg:
    st.markdown(f"""<style>.stApp{{background:linear-gradient(rgba(0,0,0,0.7),rgba(0,0,0,0.85)),url("data:image/jpg;base64,{bg}");background-size:cover;background-position:center;background-attachment:fixed}}</style>""", unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.center{color:white;font-size:28px;text-align:center;margin-top:10vh;margin-bottom:20px}

/* + BUTTON - REAL BUTTON - BLACK BOX WHITE TEXT - NO OVERLAY */
div[data-testid="stFileUploader"]{background:transparent!important;border:none!important}
div[data-testid="stFileUploader"] section{background:transparent!important;border:none!important;padding:0!important}
div[data-testid="stFileUploader"] section>div:first-child{display:none!important}
div[data-testid="stFileUploader"] section small{display:none!important}
div[data-testid="stFileUploader"] section button{
    background:#000!important;
    border:1px solid #555!important;
    border-radius:12px!important;
    height:52px!important;
    width:100%!important;
    color:white!important;
}
div[data-testid="stFileUploader"] section button svg{display:none!important}
div[data-testid="stFileUploader"] section button div p{font-size:0!important}
div[data-testid="stFileUploader"] section button div p::after{
    content:"+";
    font-size:32px!important;
    color:white!important;
    display:block!important;
}

/* ASK CHATGPT - BLACK BOX WHITE TEXT */
.stTextInput input{background:#000!important;color:white!important;border:1px solid #555!important;border-radius:12px!important;height:52px!important}
.stTextInput input::placeholder{color:white!important;opacity:0.7!important}

/* GENERATE - BLACK BOX WHITE TEXT - NO OVERLAP */
div[data-testid="stFormSubmitButton"] button{background:#000!important;color:white!important;border:1px solid #555!important;border-radius:12px!important;height:52px!important}
div[data-testid="stFormSubmitButton"] button p{color:white!important}

/* DOWNLOAD - BLACK BOX WHITE TEXT */
div[data-testid="stDownloadButton"] button{background:#000!important;color:white!important;border:1px solid #555!important;border-radius:12px!important;height:48px!important}
div[data-testid="stDownloadButton"] button p{color:white!important}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

if "last_gen" not in st.session_state:
    st.session_state.last_gen = 0
    st.session_state.gen_url = None
    st.session_state.gen_data = None

_, mid, _ = st.columns([1,2,1])
with mid:
    with st.form("chat_form", clear_on_submit=False):
        c1, c2 = st.columns([1,4])
        with c1:
            st.file_uploader("file", type=["jpg","png","webp"], label_visibility="collapsed")
        with c2:
            prompt = st.text_input("prompt", placeholder="Ask ChatGPT", label_visibility="collapsed")
        gen_clicked = st.form_submit_button("Generate")

    if gen_clicked and prompt:
        now = time.time()
        if now - st.session_state.last_gen < 46:
            st.error(f"⏳ Wait {int(46-(now-st.session_state.last_gen))} sec")
        else:
            st.session_state.last_gen = now
            enc = urllib.parse.quote(prompt + ", photorealistic, 8k")
            seed = random.randint(1, 9999999)
            url = f"{API_BASE}/{enc}?model={MODEL}&width=1024&height=1024&seed={seed}&nologo=true"
            st.session_state.gen_url = url
            try:
                st.session_state.gen_data = requests.get(url, timeout=20).content
            except:
                st.session_state.gen_data = None
            st.rerun()

    if st.session_state.gen_url:
        st.image(st.session_state.gen_url, width="stretch")
        if st.session_state.gen_data:
            b1, b2 = st.columns(2)
            with b1:
                st.markdown(f"""
                <button onclick="navigator.clipboard.writeText('{st.session_state.gen_url}');alert('Copied!')" 
                style="width:100%;height:48px;background:#000;color:white;border:1px solid #555;border-radius:12px;cursor:pointer">📋 Copy Link</button>
                """, unsafe_allow_html=True)
            with b2:
                st.download_button("⬇️ Download", data=st.session_state.gen_data, file_name="image.jpg", mime="image/jpeg", use_container_width=True)
