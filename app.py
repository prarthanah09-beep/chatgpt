import streamlit as st, urllib.parse, random, time, requests, base64
from pathlib import Path
st.set_page_config(page_title="ChatGPT", layout="wide")

API_BASE = st.secrets.get("POLLINATION_API", "https://image.pollinations.ai/prompt")
MODEL = st.secrets.get("MODEL", "flux")

# BG
p = Path("static/india.jpg")
if p.exists():
    st.markdown(f'<style>.stApp{{background:linear-gradient(rgba(0,0,0,.6),rgba(0,0,0,.8)),url("data:image/jpg;base64,{base64.b64encode(p.read_bytes()).decode()}");background-size:cover}}</style>', unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.center{color:white;font-size:28px;text-align:center;margin-top:18vh;margin-bottom:20px}

/* BLACK BOX + ONLY - NO ARROW */
div[data-testid="stFileUploader"] section{
    background:#000 !important;
    border:1px solid #555 !important;
    border-radius:12px !important;
    height:52px !important;
    padding:0 !important;
}
/* HIDE ARROW AND ALL EXTRA TEXT */
div[data-testid="stFileUploader"] svg{display:none !important}
div[data-testid="stFileUploader"] span{display:none !important}
div[data-testid="stFileUploader"] small{display:none !important}
div[data-testid="stFileUploader"] section>div:first-child{display:none !important}

div[data-testid="stFileUploader"] button{
    background:#000 !important;
    border:0 !important;
    width:100% !important;
    height:52px !important;
}
div[data-testid="stFileUploader"] button p{
    color:white !important;
    font-size:32px !important;
}

/* OTHER BLACK BOXES */
div[data-testid="stTextInput"] input{background:#000 !important;color:white !important;border:1px solid #555 !important;border-radius:12px !important;height:52px !important}
div[data-testid="stFormSubmitButton"] button, div[data-testid="stDownloadButton"] button{background:#000 !important;color:white !important;border:1px solid #555 !important;border-radius:12px !important}
div[data-testid="stFormSubmitButton"] button *{color:white !important}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

if "gen_url" not in st.session_state:
    st.session_state.gen_url=None; st.session_state.gen_data=None; st.session_state.last_gen=0

_,mid,_=st.columns([1,2,1])
with mid:
    with st.form("f"):
        c1,c2=st.columns([1,4])
        with c1:
            # THIS IS + BUTTON - NO ARROW
            st.file_uploader("+", type=["jpg","png","webp"], label_visibility="collapsed")
        with c2:
            prompt=st.text_input("p", placeholder="Ask ChatGPT", label_visibility="collapsed")
        gen=st.form_submit_button("Generate")

    if gen and prompt:
        now=time.time()
        if now-st.session_state.last_gen<46:
            st.error(f"Wait {int(46-(now-st.session_state.last_gen))} sec")
        else:
            st.session_state.last_gen=now
            url=f"{API_BASE}/{urllib.parse.quote(prompt)}?model={MODEL}&width=1024&height=1024&seed={random.randint(1,999999)}&nologo=true"
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
                st.markdown(f"""<button onclick="navigator.clipboard.writeText('{st.session_state.gen_url}')" style="width:100%;height:45px;background:#000;color:#fff;border:1px solid #555;border-radius:12px">Copy</button>""", unsafe_allow_html=True)
            with b2:
                st.download_button("Download", st.session_state.gen_data, "img.jpg", "image/jpeg", use_container_width=True)

# FORCE + AND REMOVE ARROW - MOBILE FIX
st.components.v1.html("""
<script>
const d = window.parent.document;
setInterval(()=>{
  const btn = d.querySelector('[data-testid="stFileUploader"] button p');
  if(btn){ btn.innerText = '+'; btn.style.fontSize='32px'; btn.style.color='white'; }
  d.querySelectorAll('[data-testid="stFileUploader"] svg, [data-testid="stFileUploader"] span').forEach(e=>e.style.display='none');
}, 300);
</script>
""", height=0)
