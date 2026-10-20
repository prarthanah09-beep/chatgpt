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
.center{color:white;font-size:28px;text-align:center;margin-top:12vh;margin-bottom:25px}
.fake-plus{background:#000!important;border:1px solid #333!important;border-radius:12px!important;height:52px!important;display:flex!important;align-items:center!important;justify-content:center!important;color:white!important;font-size:32px!important;pointer-events:none}
div[data-testid="stFileUploader"]{margin-top:-52px!important;opacity:0!important;height:52px!important;position:relative!important;z-index:10!important}
.stTextInput input{background:#000!important;color:white!important;border:1px solid #333!important;border-radius:12px!important;height:52px!important}
.stTextInput input::placeholder{color:white!important}
div[data-testid="stForm"]{background:transparent!important;border:none!important}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

if "last_gen" not in st.session_state:
    st.session_state.last_gen = 0
if "gen_url" not in st.session_state:
    st.session_state.gen_url = None
if "gen_data" not in st.session_state:
    st.session_state.gen_data = None

_, mid, _ = st.columns([1,2,1])
with mid:
    # FORM - so Generate does NOT go to file option
    with st.form("chat_form", clear_on_submit=False):
        c1, c2 = st.columns([1,4])
        with c1:
            st.markdown('<div class="fake-plus">+</div>', unsafe_allow_html=True)
            uploaded = st.file_uploader("file", type=["jpg","png","webp"], label_visibility="collapsed")
        with c2:
            prompt = st.text_input("prompt", placeholder="Ask ChatGPT", label_visibility="collapsed")
        
        gen_clicked = st.form_submit_button("Generate", use_container_width=True)

    if gen_clicked and prompt:
        now = time.time()
        diff = now - st.session_state.last_gen
        if diff < 46:
            wait = int(46 - diff)
            st.error(f"⏳ Wait {wait} sec - 1 image per 45 sec")
        else:
            st.session_state.last_gen = time.time()
            enc = urllib.parse.quote(prompt + ", photorealistic, 8k")
            seed = random.randint(1, 99999999)
            url = f"{API_BASE}/{enc}?model={MODEL}&width=1024&height=1024&seed={seed}&nologo=true"
            st.session_state.gen_url = url
            try:
                resp = requests.get(url, timeout=20)
                st.session_state.gen_data = resp.content
            except:
                st.session_state.gen_data = None
            st.rerun()

    # Show generated image OUTSIDE form - stays after generate
    if st.session_state.gen_url:
        st.image(st.session_state.gen_url, width="stretch")
        if st.session_state.gen_data:
            b1, b2 = st.columns(2)
            with b1:
                st.markdown(f"""<button onclick="navigator.clipboard.writeText('{st.session_state.gen_url}');alert('Copied!')" style="width:100%;height:45px;background:#000;color:white;border:1px solid #333;border-radius:10px">📋 Copy Link</button>""", unsafe_allow_html=True)
            with b2:
                st.download_button("⬇️ Download", data=st.session_state.gen_data, file_name="generated.jpg", mime="image/jpeg", use_container_width=True)
