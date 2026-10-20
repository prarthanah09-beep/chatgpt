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
    st.markdown(f"""<style>.stApp{{background:linear-gradient(rgba(0,0,0,0.75),rgba(0,0,0,0.85)),url("data:image/jpg;base64,{bg}");background-size:cover;background-position:center}}</style>""", unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.center{color:white;font-size:28px;text-align:center;margin-top:15vh;margin-bottom:25px}
.fake-plus{background:#000!important;border:1px solid #333!important;border-radius:12px!important;height:52px!important;display:flex!important;align-items:center!important;justify-content:center!important;color:white!important;font-size:32px!important}
div[data-testid="stFileUploader"]{margin-top:-52px!important;opacity:0!important;height:52px!important;position:relative!important;z-index:10!important}
.stTextInput input{background:#000!important;color:white!important;border:1px solid #333!important;border-radius:12px!important;height:52px!important}
.stTextInput input::placeholder{color:white!important}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

if "last_gen" not in st.session_state:
    st.session_state.last_gen = 0

_, mid, _ = st.columns([1,2,1])
with mid:
    c1, c2 = st.columns([1,4])
    with c1:
        st.markdown('<div class="fake-plus">+</div>', unsafe_allow_html=True)
        st.file_uploader("file", type=["jpg","png","webp"], label_visibility="collapsed")
    with c2:
        prompt = st.text_input("prompt", placeholder="Ask ChatGPT", label_visibility="collapsed")
    
    if st.button("Generate"):
        if not prompt:
            st.warning("Type something in Ask ChatGPT")
        else:
            now = time.time()
            diff = now - st.session_state.last_gen
            if diff < 46:
                wait = int(46 - diff)
                st.error(f"⏳ Wait {wait} seconds - Free limit is 1 image per 45 sec")
                # countdown
                with st.empty():
                    for i in range(wait, 0, -1):
                        st.info(f"Retrying in {i} sec...")
                        time.sleep(1)
            
            st.session_state.last_gen = time.time()
            enc = urllib.parse.quote(prompt + ", photorealistic, 8k, ultra detailed, cinematic")
            seed = random.randint(1, 99999999)
            # nologo=true removes watermark, enhance helps
            url = f"{API_BASE}/{enc}?model={MODEL}&width=1024&height=1024&seed={seed}&nologo=true&enhance=false"
            
            with st.spinner("Generating..."):
                st.image(url, width="stretch")
            
            # Check if image is limit card by fetching
            try:
                resp = requests.get(url, timeout=15)
                if resp.status_code == 200 and len(resp.content) > 10000:  # real image > 10kb
                    # Check if not yellow limit (limit image is small ~30kb but yellow)
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"""
                        <button onclick="navigator.clipboard.writeText('{url}'); alert('Copied!')" 
                        style="width:100%;height:45px;background:#000;color:white;border:1px solid #333;border-radius:10px">📋 Copy Link</button>
                        """, unsafe_allow_html=True)
                    with c2:
                        st.download_button("⬇️ Download", data=resp.content, file_name=f"img_{seed}.jpg", mime="image/jpeg", use_container_width=True)
                else:
                    st.error("Limit hit - wait 45 sec and Generate again")
            except Exception as e:
                st.error(f"Wait 45 sec then try again")
