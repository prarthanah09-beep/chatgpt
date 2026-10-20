import streamlit as st, urllib.parse, random, base64, requests
from pathlib import Path

st.set_page_config(page_title="ChatGPT", layout="wide")

# API from Secrets - hidden
API_BASE = st.secrets.get("POLLINATION_API", "https://image.pollinations.ai/prompt")
MODEL = st.secrets.get("MODEL", "flux-realism")

def get_bg():
    p = Path("static/india.jpg")
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return None

bg = get_bg()
if bg:
    st.markdown(f"""<style>.stApp{{background:linear-gradient(rgba(0,0,0,0.7),rgba(0,0,0,0.85)),url("data:image/jpg;base64,{bg}");background-size:cover;background-position:center}}</style>""", unsafe_allow_html=True)

st.markdown("""
<style>
header,footer{visibility:hidden}
.center{color:white;font-size:28px;text-align:center;margin-top:15vh;margin-bottom:25px}
.fake-plus{background:#000!important;border:1px solid #333!important;border-radius:12px!important;height:52px!important;display:flex!important;align-items:center!important;justify-content:center!important;color:white!important;font-size:32px!important}
div[data-testid="stFileUploader"]{margin-top:-52px!important;opacity:0!important;height:52px!important;position:relative!important;z-index:10!important}
.stTextInput input{background:#000!important;color:white!important;border:1px solid #333!important;border-radius:12px!important;height:52px!important}
.stTextInput input::placeholder{color:white!important}
div.stButton>button{background:white!important;color:black!important;border-radius:25px!important;width:100%;height:50px;font-weight:700!important}
.download-btn{background:#000!important;color:white!important;border:1px solid #333!important}
.copy-btn{background:#000!important;color:white!important;border:1px solid #333!important}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

_, mid, _ = st.columns([1,2,1])
with mid:
    c1, c2 = st.columns([1,4])
    with c1:
        st.markdown('<div class="fake-plus">+</div>', unsafe_allow_html=True)
        st.file_uploader("file", type=["jpg","png","webp"], label_visibility="collapsed")
    with c2:
        prompt = st.text_input("prompt", placeholder="Ask ChatGPT", label_visibility="collapsed")
    
    if st.button("Generate"):
        if prompt:
            enc = urllib.parse.quote(prompt + ", photorealistic, 8k, ultra detailed")
            seed = random.randint(1, 9999999)
            url = f"{API_BASE}/{enc}?model={MODEL}&width=1024&height=1024&seed={seed}&nologo=true&enhance=true"
            
            # Show image - NO API LINK
            st.image(url, use_container_width=True)
            
            # Fetch image for download
            try:
                img_data = requests.get(url).content
                
                b1, b2 = st.columns(2)
                with b1:
                    # COPY LINK BUTTON
                    st.markdown(f"""
                    <button onclick="navigator.clipboard.writeText('{url}'); alert('Link Copied!')" 
                    style="width:100%;height:45px;background:#000;color:white;border:1px solid #333;border-radius:10px;cursor:pointer">
                    📋 Copy Link
                    </button>
                    """, unsafe_allow_html=True)
                
                with b2:
                    st.download_button(
                        "⬇️ Download",
                        data=img_data,
                        file_name=f"generated_{seed}.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
            except:
                st.error("Failed to load buttons, try again")
