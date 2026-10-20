import streamlit as st, requests, urllib.parse, random

st.set_page_config(page_title="ChatGPT", layout="wide")
st.markdown("<style>.stApp{background:#000!important}header,footer{visibility:hidden}.center{color:white;font-size:32px;text-align:center;margin-top:100px;margin-bottom:30px}div.stButton>button{background:white!important;color:black!important;border-radius:25px!important;width:100%;height:50px;font-weight:800!important}</style>", unsafe_allow_html=True)

st.markdown('<div class="center">What can I help with?</div>', unsafe_allow_html=True)

_, col, _ = st.columns([1,2,1])
with col:
    uploaded = st.file_uploader("📎 File", type=["jpg","png","webp"])
    if uploaded:
        st.image(uploaded, use_container_width=True)
    
    prompt = st.text_area("Ask", placeholder="Ask ChatGPT", value="Real Indian woman in saree, photorealistic, 8k", height=100, label_visibility="collapsed")
    
    if st.button("ASK AI - GENERATE REAL"):
        encoded = urllib.parse.quote(prompt + ", ultra realistic, real skin, 8k, DSLR")
        seed = random.randint(1, 9999999)
        url = f"https://image.pollinations.ai/prompt/{encoded}?model=flux-realism&width=1024&height=1024&seed={seed}&nologo=true&enhance=true"
        
        # ONLY DIRECT IMAGE - ALWAYS WORKS
        st.image(url, caption=f"REAL - flux-realism - {seed}", use_container_width=True)
        st.success("✅ REAL Image")
        st.code(url, language="text")
