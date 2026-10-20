import streamlit as st, urllib.parse, random, time, requests, base64
from pathlib import Path

st.set_page_config(page_title="ChatGPT", layout="wide", initial_sidebar_state="collapsed")

API_BASE = st.secrets.get("POLLINATION_API", "https://image.pollinations.ai/prompt")
MODEL = st.secrets.get("MODEL", "flux")

# Background image
p = Path("static/india.jpg")
if p.exists():
    b64 = base64.b64encode(p.read_bytes()).decode()
    st.markdown(f"""
    <style>
    .stApp{{
        background:linear-gradient(rgba(0,0,0,0.6),rgba(0,0,0,0.8)),url("data:image/jpg;base64,{b64}");
        background-size:cover;
        background-position:center;
        background-attachment:fixed;
    }}
    /* HIDE Made with AI BADGE - TOP RIGHT */
    .stApp::before{{
        content:"";
        position:fixed;
        top:0;
        right:0;
        width:300px;
        height:80px;
        background:#080e1f;
        z-index:99999;
        pointer-events:none;
    }}
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.center{color:white;font-size:28px;text-align:center;margin-top:18vh;margin-bottom:20px;font-weight:600}

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
    border:1px solid #555 !important;
    border-radius:12px !important;
    height:52px !important;
}
div[data-testid="stTextInput"] input::placeholder{color:#aaa !important}

div[data-testid="stFormSubmitButton"] button, div[data-testid="stDownloadButton"] button{
    background:#000 !important;
    color:white !important;
    border:1px solid #555 !important;
    border-radius:12px !important;
    height:45px !important;
}
div[data-testid="stFormSubmitButton"] button *, div[data-testid="stDownloadButton"] button *{color:white !important}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

if "gen_url" not in st.session_state:
    st.session_state.gen_url=None
    st.session_state.gen_data=None
    st.session_state.last_gen=0

_,mid,_=st.columns([1,2,1])
with mid:
    with st.form("chat_form"):
        c1,c2=st.columns([1,4])
        with c1:
            st.markdown('<div class="plus-only">+</div>', unsafe_allow_html=True)
        with c2:
            prompt=st.text_input("prompt", placeholder="Ask ChatGPT", label_visibility="collapsed")
        gen=st.form_submit_button("Generate")

    if gen and prompt and prompt.strip():
        now=time.time()
        if now - st.session_state.last_gen < 46:
            st.error(f"Wait {int(46-(now-st.session_state.last_gen))} sec")
        else:
            st.session_state.last_gen=now
            with st.spinner("Generating..."):
                url=f"{API_BASE}/{urllib.parse.quote(prompt.strip())}?model={MODEL}&width=1024&height=1024&seed={random.randint(1,9999999)}&nologo=true"
                st.session_state.gen_url=url
                try:
                    r=requests.get(url, timeout=30)
                    st.session_state.gen_data=r.content if r.status_code==200 else None
                except Exception as e:
                    st.error(str(e))
                    st.session_state.gen_data=None
            st.rerun()

    if st.session_state.gen_url:
        st.image(st.session_state.gen_url, use_container_width=True)
        if st.session_state.gen_data:
            b1,b2=st.columns(2)
            with b1:
                st.markdown(f"""
                <button onclick="navigator.clipboard.writeText('{st.session_state.gen_url}');alert('Copied!')" 
                style="width:100%;height:48px;background:#000;color:white;border:1px solid #555;border-radius:12px;cursor:pointer">
                📋 Copy</button>
                """, unsafe_allow_html=True)
            with b2:
                st.download_button("⬇️ Download", data=st.session_state.gen_data, file_name="generated.jpg", mime="image/jpeg", use_container_width=True)
