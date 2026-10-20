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

/* PURE PLUS BUTTON - NO ARROW */
.plus-box{
    background:#000;
    border:1px solid #555;
    border-radius:12px;
    height:52px;
    width:100%;
    display:flex;
    align-items:center;
    justify-content:center;
    cursor:pointer;
}
.plus-box label{
    color:white;
    font-size:36px;
    font-weight:300;
    cursor:pointer;
    width:100%;
    height:100%;
    display:flex;
    align-items:center;
    justify-content:center;
}
.plus-box input{display:none}

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
            # THIS IS PURE + SIGN - WILL OPEN GALLERY ON MOBILE
            st.markdown('<div class="plus-box"><label for="file">+<input type="file" id="file" accept="image/*"></label></div>', unsafe_allow_html=True)
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
            st.download_button("Download", st.session_state.data, "image.jpg", "image/jpeg", use_container_width=True)
