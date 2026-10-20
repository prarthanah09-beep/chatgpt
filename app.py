import streamlit as st, urllib.parse, random, time, requests, base64
from pathlib import Path
st.set_page_config(page_title="ChatGPT", layout="wide")

API_BASE = st.secrets.get("POLLINATION_API", "https://image.pollinations.ai/prompt")
MODEL = st.secrets.get("MODEL", "flux")

p = Path("static/india.jpg")
if p.exists():
    b64 = base64.b64encode(p.read_bytes()).decode()
    st.markdown(f'<style>.stApp{{background:linear-gradient(rgba(0,0,0,0.6),rgba(0,0,0,0.8)),url("data:image/jpg;base64,{b64}");background-size:cover;background-position:center top;background-attachment:fixed}}</style>', unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.center{color:white;font-size:28px;text-align:center;margin-top:15vh;margin-bottom:20px;font-weight:600}

/* FORCE COLUMNS TO STAY SIDE BY SIDE ON MOBILE */
div[data-testid="stHorizontalBlock"]{
    display:flex !important;
    flex-direction:row !important;
    flex-wrap:nowrap !important;
    gap:8px !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child{
    flex:0 0 60px !important;
    min-width:60px !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child{
    flex:1 !important;
}

.plus-only{
    background:#000 !important;
    border:1px solid #666 !important;
    border-radius:12px !important;
    height:52px !important;
    width:100% !important;
    color:white !important;
    font-size:30px !important;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
}

/* INPUT - BLACK BOX */
div[data-testid="stTextInput"] input{
    background:#000 !important;
    color:white !important;
    -webkit-text-fill-color:white !important;
    border:1px solid #666 !important;
    border-radius:12px !important;
    height:52px !important;
    font-size:16px !important;
}

/* PLACEHOLDER WHITE - MOBILE FIX */
div[data-testid="stTextInput"] input::placeholder{
    color:white !important;
    -webkit-text-fill-color:white !important;
    opacity:1 !important;
}
div[data-testid="stTextInput"] input::-webkit-input-placeholder{
    color:white !important;
    -webkit-text-fill-color:white !important;
    opacity:1 !important;
}
div[data-testid="stTextInput"] input::-moz-placeholder{
    color:white !important;
    -webkit-text-fill-color:white !important;
    opacity:1 !important;
}
div[data-testid="stTextInput"] input:-ms-input-placeholder{
    color:white !important;
    -webkit-text-fill-color:white !important;
}

div[data-testid="stFormSubmitButton"] button{
    background:#000 !important;
    color:white !important;
    border:1px solid #666 !important;
    border-radius:12px !important;
    height:44px !important;
}
div[data-testid="stFormSubmitButton"] button *{color:white !important}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

if "gen_url" not in st.session_state:
    st.session_state.gen_url=None; st.session_state.gen_data=None; st.session_state.last_gen=0

_,mid,_=st.columns([1,2,1])
with mid:
    with st.form("f", clear_on_submit=False):
        c1,c2=st.columns([1,4])
        with c1:
            st.markdown('<div class="plus-only">+</div>', unsafe_allow_html=True)
        with c2:
            prompt=st.text_input("p", placeholder="Ask ChatGPT", label_visibility="collapsed", key="prompt_input")
        gen=st.form_submit_button("Generate", use_container_width=False)

    if gen:
        if not prompt or not prompt.strip():
            st.warning("Type something in Ask ChatGPT")
        else:
            now=time.time()
            if now - st.session_state.last_gen < 46:
                st.error(f"Wait {int(46-(now-st.session_state.last_gen))}s")
            else:
                st.session_state.last_gen=now
                with st.spinner("Generating..."):
                    url=f"{API_BASE}/{urllib.parse.quote(prompt.strip())}?model={MODEL}&width=1024&height=1024&seed={random.randint(1,9999999)}&nologo=true"
                    st.session_state.gen_url=url
                    try:
                        r=requests.get(url, timeout=60)
                        st.session_state.gen_data=r.content if r.status_code==200 else None
                    except Exception as e:
                        st.error(f"Error: {e}")
                st.rerun()

    if st.session_state.gen_url:
        st.image(st.session_state.gen_url, use_container_width=True)
        if st.session_state.gen_data:
            b1,b2=st.columns(2)
            with b1:
                st.download_button("Download", st.session_state.gen_data, "img.jpg", "image/jpeg", use_container_width=True)
            with b2:
                st.markdown(f'<button onclick="navigator.clipboard.writeText(\'{st.session_state.gen_url}\');alert(\'Copied\')" style="width:100%;height:46px;background:#000;color:white;border:1px solid #666;border-radius:12px">Copy Link</button>', unsafe_allow_html=True)

# FORCE PLACEHOLDER WHITE ON MOBILE VIA JS
st.components.v1.html("""
<script>
const doc = window.parent.document;
setInterval(()=>{
  const inputs = doc.querySelectorAll('input[placeholder=\"Ask ChatGPT\"]');
  inputs.forEach(i=>{
    i.style.color='white';
    i.style.webkitTextFillColor='white';
    i.placeholder='Ask ChatGPT';
  });
}, 500);
</script>
""", height=0)
