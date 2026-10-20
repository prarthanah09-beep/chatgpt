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
    st.markdown(f"""<style>.stApp{{background:linear-gradient(rgba(0,0,0,0.6),rgba(0,0,0,0.8)),url("data:image/jpg;base64,{bg}");background-size:cover}}</style>""", unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.center{color:white;font-size:28px;text-align:center;margin-top:18vh;margin-bottom:25px}

/* REAL FILE UPLOADER = BLACK BOX WITH ONLY + */
div[data-testid="stFileUploader"] section{
    background:#000 !important;
    border:1px solid #555 !important;
    border-radius:12px !important;
    height:52px !important;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
}
/* Hide drag text and limit text */
div[data-testid="stFileUploader"] section>div:first-child, 
div[data-testid="stFileUploader"] small{display:none !important}

/* Hide the small upload arrow icon */
div[data-testid="stFileUploader"] svg, 
div[data-testid="stFileUploader"] section span{display:none !important}

/* The button itself - make it full black */
div[data-testid="stFileUploader"] section button{
    background:#000 !important;
    border:none !important;
    width:100% !important;
    height:52px !important;
}
/* Force + text - ONLY + */
div[data-testid="stFileUploader"] section button div p{
    font-size:0 !important;
}
div[data-testid="stFileUploader"] section button div p::after{
    content:"+";
    font-size:32px !important;
    color:white !important;
}

/* ASK CHATGPT BLACK */
div[data-testid="stTextInput"] input{
    background:#000 !important;
    color:white !important;
    border:1px solid #555 !important;
    border-radius:12px !important;
    height:52px !important;
}

/* GENERATE BLACK */
div[data-testid="stFormSubmitButton"] button, div[data-testid="stDownloadButton"] button{
    background:#000 !important;
    color:white !important;
    border:1px solid #555 !important;
    border-radius:12px !important;
}
div[data-testid="stFormSubmitButton"] button *, div[data-testid="stDownloadButton"] button *{color:white !important}
</style>

<script>
// FORCE ONLY + ON MOBILE - JS FIX
setTimeout(function(){
    const check = setInterval(function(){
        const btn = document.querySelector('[data-testid="stFileUploader"] button div p');
        if(btn){
            btn.innerHTML = '+';
            btn.style.fontSize = '32px';
            btn.style.color = 'white';
        }
        const svgs = document.querySelectorAll('[data-testid="stFileUploader"] svg');
        svgs.forEach(s=>s.style.display='none');
    }, 500);
}, 1000);
</script>
""", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

if "gen_url" not in st.session_state:
    st.session_state.gen_url=None; st.session_state.gen_data=None; st.session_state.last_gen=0

_, mid, _ = st.columns([1,2,1])
with mid:
    with st.form("chat_form"):
        c1,c2=st.columns([1,4])
        with c1:
            st.file_uploader(" ", type=["jpg","png","webp","jpeg"], label_visibility="collapsed")
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
                pass
            st.rerun()

    if st.session_state.gen_url:
        st.image(st.session_state.gen_url, use_container_width=True)
        if st.session_state.gen_data:
            b1,b2=st.columns(2)
            with b1:
                st.markdown(f"""<button onclick="navigator.clipboard.writeText('{st.session_state.gen_url}')" style="width:100%;height:48px;background:#000;color:white;border:1px solid #555;border-radius:12px">📋 Copy</button>""", unsafe_allow_html=True)
            with b2:
                st.download_button("⬇️ Download", data=st.session_state.gen_data, file_name="img.jpg", mime="image/jpeg", use_container_width=True)
