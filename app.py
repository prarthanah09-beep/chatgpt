import streamlit as st, urllib.parse, random, base64, time, requests
from pathlib import Path

st.set_page_config(page_title="ChatGPT", layout="wide")

API_BASE = st.secrets.get("POLLINATION_API", "https://image.pollinations.ai/prompt")
MODEL = st.secrets.get("MODEL", "flux")

bg_file = Path("static/india.jpg")
if bg_file.exists():
    import base64
    bg = base64.b64encode(bg_file.read_bytes()).decode()
    st.markdown(f'<style>.stApp{{background:linear-gradient(rgba(0,0,0,0.6),rgba(0,0,0,0.8)),url("data:image/jpg;base64,{bg}");background-size:cover}}</style>', unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.center{color:white;font-size:28px;text-align:center;margin-top:18vh;margin-bottom:20px}

/* MAKE FILE UPLOADER LOOK LIKE + BUTTON */
div[data-testid="stFileUploader"] section{
    background:#000 !important;
    border:1px solid #666 !important;
    border-radius:12px !important;
    height:52px !important;
    min-height:52px !important;
    padding:0 !important;
    display:flex;
    align-items:center;
    justify-content:center;
}
div[data-testid="stFileUploader"] section>div, div[data-testid="stFileUploader"] small{display:none !important}
div[data-testid="stFileUploader"] svg{display:none !important}
div[data-testid="stFileUploader"] button{
    background:transparent !important;
    border:none !important;
    width:100% !important;
}
div[data-testid="stFileUploader"] button p{
    color:white !important;
    font-size:30px !important;
}

div[data-testid="stTextInput"] input{background:#000 !important;color:white !important;border:1px solid #666 !important;border-radius:12px !important;height:52px !important}
div[data-testid="stFormSubmitButton"] button, div[data-testid="stDownloadButton"] button{background:#000 !important;color:white !important;border:1px solid #666 !important;border-radius:12px !important}
div[data-testid="stFormSubmitButton"] button *{color:white !important}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

if "gen_url" not in st.session_state:
    st.session_state.gen_url=None; st.session_state.gen_data=None; st.session_state.last_gen=0

_,mid,_=st.columns([1,2,1])
with mid:
    with st.form("form"):
        c1,c2=st.columns([1,4])
        with c1:
            up=st.file_uploader("+", type=["jpg","png","webp","jpeg"], label_visibility="collapsed")
        with c2:
            prompt=st.text_input("p", placeholder="Ask ChatGPT", label_visibility="collapsed")
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
            except Exception as e:
                st.error(str(e))
            st.rerun()
    
    if st.session_state.gen_url:
        st.image(st.session_state.gen_url, use_container_width=True)
        if st.session_state.gen_data:
            a,b=st.columns(2)
            with a:
                st.markdown(f'<button onclick="navigator.clipboard.writeText(\'{st.session_state.gen_url}\')" style="width:100%;height:45px;background:#000;color:#fff;border:1px solid #666;border-radius:12px">Copy</button>', unsafe_allow_html=True)
            with b:
                st.download_button("Download", st.session_state.gen_data, "img.jpg", "image/jpeg", use_container_width=True)

# JS TO FORCE + SIGN - WORKS ON MOBILE
st.components.v1.html("""
<script>
const parent = window.parent.document;
setInterval(()=>{
  const p = parent.querySelector('[data-testid="stFileUploader"] button p');
  if(p && p.innerText !== '+'){
    p.innerText = '+';
    p.style.fontSize = '30px';
    p.style.color = 'white';
  }
  const svgs = parent.querySelectorAll('[data-testid="stFileUploader"] svg');
  svgs.forEach(s=>s.style.display='none');
}, 300);
</script>
""", height=0)
