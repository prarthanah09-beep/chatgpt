import streamlit as st, urllib.parse, random

st.set_page_config(page_title="ChatGPT", layout="wide")

st.markdown("""
<style>
.stApp{background:#000!important}
header,footer{visibility:hidden}
.block-container{padding-top:20px!important}
.center{color:white;font-size:28px;font-weight:500;text-align:center;margin-top:80px;margin-bottom:30px}
/* ONLY + SIGN - BLACK BOX WHITE TEXT */
div[data-testid="stFileUploader"]{background:#000!important;border:1px solid #333!important;border-radius:12px!important}
div[data-testid="stFileUploader"] *{color:white!important}
div[data-testid="stFileUploader"] button{background:#000!important;color:white!important;border:1px solid #555!important;border-radius:8px!important}
div[data-testid="stFileUploader"] small{display:none!important}
.stTextInput input{background:#2f2f2f!important;color:white!important;border-radius:12px!important;border:1px solid #444!important;height:50px}
div.stButton>button{background:white!important;color:black!important;border-radius:25px!important;width:100%;height:50px;font-weight:800!important}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

_, mid, _ = st.columns([1,2,1])
with mid:
    # EXACT LIKE SCREENSHOT - + sign only
    col1, col2 = st.columns([1,4])
    with col1:
        uploaded = st.file_uploader(" ", type=["jpg","png","webp"], label_visibility="collapsed")
    with col2:
        prompt = st.text_input(" ", placeholder="Ask ChatGPT", label_visibility="collapsed")
    
    if uploaded:
        st.image(uploaded, use_container_width=True)
    
    if st.button("Generate") and prompt:
        enc = urllib.parse.quote(prompt + ", photorealistic, ultra realistic, real skin, 8k")
        seed = random.randint(1, 9999999)
        url = f"https://image.pollinations.ai/prompt/{enc}?model=flux-realism&width=1024&height=1024&seed={seed}&nologo=true&enhance=true"
        st.image(url, caption=f"REAL - {seed}", use_container_width=True)
        st.markdown(f"[Open HD]({url})")
