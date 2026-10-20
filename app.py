import streamlit as st, urllib.parse, random, requests, base64
from pathlib import Path

st.set_page_config(page_title="ChatGPT", layout="wide")

# BACKGROUND
p = Path("static/india.jpg")
if p.exists():
    b64 = base64.b64encode(p.read_bytes()).decode()
    st.markdown(f'<style>.stApp{{background:linear-gradient(rgba(0,0,0,0.5),rgba(0,0,0,0.7)),url("data:image/jpg;base64,{b64}");background-size:cover;background-position:center}}</style>', unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.center{color:white;font-size:28px;text-align:center;margin-top:18vh;margin-bottom:22px;font-weight:600}

/* MAKE FILE UPLOADER LOOK LIKE + BUTTON ONLY */
div[data-testid="stFileUploader"]{width:100% !important}
div[data-testid="stFileUploader"] section{
    background:#000 !important;
    border:1px solid #555 !important;
    border-radius:12px !important;
    height:52px !important;
    min-height:52px !important;
    padding:0 !important;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
}
div[data-testid="stFileUploader"] svg{display:none !important}
div[data-testid="stFileUploader"] span{display:none !important}
div[data-testid="stFileUploader"] small{display:none !important}
div[data-testid="stFileUploader"] div[data-testid="stFileUploaderFileName"]{display:none !important}

div[data-testid="stTextInput"] input{
    background:#000 !important;
    color:white !important;
    -webkit-text-fill-color:white !important;
    border:1px solid #555 !important;
    border-radius:12px !important;
    height:52px !important;
}
div[data-testid="stTextInput"] input::placeholder{
    color:white !important;
    -webkit-text-fill-color:white !important;
    opacity:1 !important;
}
div[data-testid="stFormSubmitButton"] button{
    background:#000 !important;
    color:white !important;
    border:1px solid #555 !important;
    border-radius:12px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

if "url" not in st.session_state:
    st.session_state.url=None
    st.session_state.data=None

_,mid,_=st.columns([1,2,1])
with mid:
    with st.form("f"):
        c1,c2=st.columns([1,4])
        with c1:
            up = st.file_uploader("", type=["jpg","png","webp","jpeg"], label_visibility="collapsed", key="plus")
        with c2:
            prompt=st.text_input("", placeholder="Ask ChatGPT", label_visibility="collapsed")
        gen=st.form_submit_button("Generate", use_container_width=True)

    if gen and prompt and prompt.strip():
        url=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt.strip())}?model=flux&width=1024&height=1024&seed={random.randint(1,9999999)}&nologo=true"
        r=requests.get(url, timeout=60)
        st.session_state.url=url
        st.session_state.data=r.content
        st.rerun()

    if st.session_state.url:
        st.image(st.session_state.url, use_container_width=True)
        if st.session_state.data:
            st.download_button("Download", st.session_state.data, "image.jpg", use_container_width=True)

# JS THAT CREATES PLUS SIGN
st.components.v1.html("""
<script>
const doc = window.parent.document;
function makePlus(){
  const sec = doc.querySelector('div[data-testid="stFileUploader"] section button');
  if(sec){
    const p = sec.querySelector('p');
    if(p){
      p.innerText = '+';
      p.style.color = 'white';
      p.style.fontSize = '34px';
      p.style.fontWeight = '300';
      p.style.lineHeight = '52px';
    }
    // Remove any other text nodes that are arrow
    const spans = doc.querySelectorAll('div[data-testid="stFileUploader"] span, div[data-testid="stFileUploader"] small, div[data-testid="stFileUploader"] svg');
    spans.forEach(s=> s.style.display='none');
  }
}
setInterval(makePlus, 200);
makePlus();
</script>
""", height=0)
