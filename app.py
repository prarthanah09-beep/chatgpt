import streamlit as st, urllib.parse, random, requests, base64
from pathlib import Path

st.set_page_config(page_title="ChatGPT", layout="wide")

p = Path("static/india.jpg")
if p.exists():
    b64 = base64.b64encode(p.read_bytes()).decode()
    st.markdown(f'<style>.stApp{{background:linear-gradient(rgba(0,0,0,0.5),rgba(0,0,0,0.7)),url("data:image/jpg;base64,{b64}");background-size:cover;background-position:center}}</style>', unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.center{color:white;font-size:28px;text-align:center;margin-top:18vh;margin-bottom:22px;font-weight:600}

/* PLUS UPLOADER - ONLY + NO ARROW */
div[data-testid="stFileUploader"]{width:100%}
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
div[data-testid="stFileUploader"] section > div{margin:0 !important}
div[data-testid="stFileUploader"] svg{display:none !important}
div[data-testid="stFileUploader"] span{display:none !important}
div[data-testid="stFileUploader"] small{display:none !important}
div[data-testid="stFileUploader"] section > div:first-child{display:none !important}

div[data-testid="stFileUploader"] button{
    background:transparent !important;
    border:0 !important;
    width:100% !important;
    height:52px !important;
}
div[data-testid="stFileUploader"] button p{
    color:white !important;
    font-size:32px !important;
    font-weight:300 !important;
}

/* INPUT WHITE TEXT */
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
            # THIS + WILL OPEN GALLERY ON MOBILE
            uploaded = st.file_uploader("plus", type=["jpg","jpeg","png","webp"], label_visibility="collapsed", key="plus_mobile")
        with c2:
            prompt=st.text_input("p", placeholder="Ask ChatGPT", label_visibility="collapsed")
        gen=st.form_submit_button("Generate")

    if gen and prompt and prompt.strip():
        url=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt.strip())}?model=flux&width=1024&height=1024&seed={random.randint(1,9999999)}&nologo=true"
        try:
            r=requests.get(url, timeout=60)
            st.session_state.url=url
            st.session_state.data=r.content
            st.rerun()
        except Exception as e:
            st.error(str(e))

    if uploaded:
        st.success(f"Selected: {uploaded.name}")
        st.image(uploaded, width=200)

    if st.session_state.url:
        st.image(st.session_state.url, use_container_width=True)
        if st.session_state.data:
            st.download_button("Download", st.session_state.data, "image.jpg", "image/jpeg", use_container_width=True)

# FORCE + AND REMOVE ARROW - MOBILE
st.components.v1.html("""
<script>
const doc = window.parent.document;
setInterval(()=>{
  const btnP = doc.querySelector('[data-testid="stFileUploader"] button p');
  if(btnP){
    btnP.innerText='+';
    btnP.style.fontSize='32px';
    btnP.style.color='white';
  }
  doc.querySelectorAll('[data-testid="stFileUploader"] svg, [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small').forEach(e=>{
    e.style.display='none';
  });
}, 300);
</script>
""", height=0)
