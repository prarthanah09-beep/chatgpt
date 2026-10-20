import streamlit as st, urllib.parse, random, requests, base64
from pathlib import Path

st.set_page_config(page_title="ChatGPT", layout="wide")

# --- LOAD YOUR CLEAN BACKGROUND ---
p = Path("static/india.jpg")
if p.exists():
    b64 = base64.b64encode(p.read_bytes()).decode()
    st.markdown(f"""
    <style>
    .stApp{{
        background:linear-gradient(rgba(0,0,0,0.5),rgba(0,0,0,0.7)),url("data:image/jpg;base64,{b64}");
        background-size:cover;
        background-position:center;
        background-attachment:fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.center{color:white;font-size:28px;text-align:center;margin-top:18vh;margin-bottom:22px;font-weight:600}

.plus-only{
  background:#000;
  border:1px solid #555;
  border-radius:12px;
  height:52px;
  width:100%;
  color:white;
  font-size:32px;
  display:flex;
  align-items:center;
  justify-content:center;
}

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
            st.markdown('<div class="plus-only">+</div>', unsafe_allow_html=True)
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

    if st.session_state.url:
        st.image(st.session_state.url, use_container_width=True)
        if st.session_state.data:
            st.download_button("Download", st.session_state.data, "image.jpg", "image/jpeg", use_container_width=True)

st.components.v1.html("""
<script>
const d=window.parent.document;
setInterval(()=>{
  d.querySelectorAll('input[placeholder=\"Ask ChatGPT\"]').forEach(i=>{
    i.style.color='white';
    i.style.webkitTextFillColor='white';
  });
}, 500);
</script>
""", height=0)
