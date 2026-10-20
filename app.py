import streamlit as st, urllib.parse, random, requests, time

st.set_page_config(page_title="ChatGPT", layout="centered")

# --- CSS - MOBILE + DESKTOP BOTH WORKING ---
st.markdown("""
<style>
header,footer{display:none !important}
.stApp{background:#000 !important}

/* CENTER TEXT */
.title{color:white;font-size:28px;text-align:center;margin-top:15vh;margin-bottom:25px;font-weight:600}

/* PLUS BUTTON - ONLY + NO ARROW */
.plus{
  background:#111;
  border:1px solid #444;
  border-radius:12px;
  height:52px;
  color:white;
  font-size:30px;
  display:flex;
  align-items:center;
  justify-content:center;
}

/* INPUT */
div[data-testid="stTextInput"] input{
  background:#111 !important;
  border:1px solid #444 !important;
  border-radius:12px !important;
  height:52px !important;
  color:white !important;
}

/* PLACEHOLDER WHITE - WORKS ON MOBILE */
input::placeholder{color:white !important;opacity:1 !important}
::-webkit-input-placeholder{color:white !important;opacity:1 !important}
::-moz-placeholder{color:white !important;opacity:1 !important}
:-ms-input-placeholder{color:white !important;opacity:1 !important}

/* BUTTONS */
div[data-testid="stFormSubmitButton"] button{
  background:#111 !important;
  color:white !important;
  border:1px solid #444 !important;
  border-radius:12px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">What can I help with?</div>', unsafe_allow_html=True)

if "url" not in st.session_state:
    st.session_state.url=None
    st.session_state.data=None

with st.form("f"):
    c1,c2 = st.columns([1,4])
    with c1:
        st.markdown('<div class="plus">+</div>', unsafe_allow_html=True)
    with c2:
        prompt = st.text_input("x", placeholder="Ask ChatGPT", label_visibility="collapsed")
    gen = st.form_submit_button("Generate", use_container_width=True)

if gen and prompt:
    with st.spinner("Generating..."):
        api = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?model=flux&width=1024&height=1024&seed={random.randint(1,9999999)}&nologo=true"
        try:
            r = requests.get(api, timeout=60)
            if r.status_code==200:
                st.session_state.url=api
                st.session_state.data=r.content
            else:
                st.error(f"API Error {r.status_code}")
        except Exception as e:
            st.error(str(e))

if st.session_state.url:
    st.image(st.session_state.url, use_container_width=True)
    if st.session_state.data:
        st.download_button("Download", st.session_state.data, "image.jpg", "image/jpeg", use_container_width=True)

# FORCE WHITE PLACEHOLDER ON MOBILE
st.components.v1.html("""
<script>
setInterval(()=>{
  let d=window.parent.document;
  d.querySelectorAll('input').forEach(i=>{
    if(i.placeholder.includes('Ask')){
      i.style.color='white';
      i.style.setProperty('-webkit-text-fill-color','white','important');
    }
  });
}, 600);
</script>
""", height=0)
