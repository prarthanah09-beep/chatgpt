import os, uuid, base64
from pathlib import Path
from urllib.parse import quote
import requests
import streamlit as st
import streamlit.components.v1 as components

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
GENERATED_DIR = STATIC_DIR / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = os.getenv("POLLINATIONS_API_KEY","").strip()
if not API_KEY:
    try: API_KEY = st.secrets.get("POLLINATIONS_API_KEY","").strip()
    except: pass

st.set_page_config(page_title="Indian AI", layout="centered")

def copy_button(text,key):
    enc=base64.b64encode(text.encode()).decode()
    safe="".join(c for c in str(key) if c.isalnum() or c in "_-")
    components.html(f"""<button id="c_{safe}" style="background:#000;color:#fff;border:1px solid #666;border-radius:8px;padding:8px 16px">Copy</button>
    <script>const b=document.getElementById("c_{safe}");b.onclick=async()=>{{let t=atob("{enc}");try{{await navigator.clipboard.writeText(new TextDecoder().decode(Uint8Array.from(t,c=>c.charCodeAt(0))));b.innerText="Copied!"}}catch{{b.innerText="Failed"}}}};</script>""",height=45)

# BACKGROUND IMAGE - ALWAYS SHOW
bp = STATIC_DIR / "india.jpg"
if bp.exists():
    b64 = base64.b64encode(bp.read_bytes()).decode()
    bg_css = f'''
    background-image: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.75)), url("data:image/jpeg;base64,{b64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-repeat: no-repeat;
    '''
else:
    bg_css = "background:#000!important;"

st.markdown(f"""
<style>
.stApp{{{bg_css}}}
.stApp::before{{content:"";position:fixed;inset:0;background:rgba(0,0,0,0.2);z-index:-1;}}
h1{{color:#fff!important;text-align:center}}
p,span,div,li,label{{color:#fff!important}}
div[data-testid="stTextInput"] input{{background:#000!important;color:#fff!important;-webkit-text-fill-color:#fff!important;border:1px solid #666!important;border-radius:12px!important}}
div[data-testid="stVerticalBlockBorderWrapper"],div[data-testid="stContainer"],div[data-testid="stForm"],div[data-testid="stPopoverBody"],div[data-testid="stChatMessage"],div[data-testid="stFileUploader"]{{background:#000!important;border:1px solid #444!important;border-radius:12px!important}}
div[data-baseweb="select"],div[data-baseweb="select"]>div,div[role="listbox"]{{background:#000!important;color:#fff!important}}
div[data-testid="stCode"],div[data-testid="stCode"] pre{{background:#000!important;color:#fff!important;border:1px solid #444!important}}
.stButton button,.stDownloadButton button,div[data-testid="stFormSubmitButton"] button{{background:#000!important;color:#fff!important;border:1px solid #666!important}}
section[data-testid="stFileUploaderDropzone"]{{background:#000!important;border:1px dashed #555!important}}
</style>""",unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages=[]
if "mode" not in st.session_state: st.session_state.mode="Both"
if "preset_prompt" not in st.session_state: st.session_state.preset_prompt=""

def generate_text(p):
    r=requests.get(f"https://text.pollinations.ai/{quote(p)}",timeout=90)
    if r.status_code==200 and r.text.strip(): return r.text.strip()
    raise RuntimeError("Failed")

def generate_image(p):
    hdr={"Authorization":f"Bearer {API_KEY}"} if API_KEY else {}
    for url in [f"https://image.pollinations.ai/prompt/{quote(p)}?width=1024&height=1024&model=flux&nologo=true", f"https://gen.pollinations.ai/image/{quote(p)}"]:
        try:
            r=requests.get(url,params={"width":1024,"height":1024,"model":"flux"},headers=hdr,timeout=120)
            if r.status_code==200 and len(r.content)>4000:
                path=GENERATED_DIR/f"image_{uuid.uuid4().hex}.jpg"
                path.write_bytes(r.content)
                return str(path)
        except: continue
    raise RuntimeError("Image failed")

PRESETS = {
"Spirited Away Buns": "Spirited Away steamed pork buns, photorealistic real food, fluffy baozi, steam rising, 8k food photography, black background",
"Howl's Breakfast": "Howl's Moving Castle breakfast, real fried eggs and bacon sizzling in cast iron pan, photorealistic, 8k",
"Ponyo Ramen": "Ponyo ramen, real ham ramen with boiled egg, steaming hot, photorealistic",
"Oggy Real Cat": "Oggy from Oggy and the Cockroaches, photorealistic real blue-grey fluffy cat standing like human, ultra detailed fur, 8k, black background",
"Tom & Jerry Real": "Tom and Jerry in real life, photorealistic grey cat and brown mouse fighting in kitchen, ultra detailed fur, 8k",
"Chota Bheem Real": "Chota Bheem in real life, photorealistic 9 year old Indian boy with dhoti, laddoo in hand, Dholakpur, 8k",
"Motu Patlu Real": "Motu Patlu in real life, photorealistic two Indian men, one fat bald with moustache eating samosa, 8k",
"Shin Chan Real": "Shin Chan in real life, photorealistic 5 year old boy, funny face, 8k"
}

st.title("Indian AI")

with st.popover("☰"):
    st.selectbox("",["Both","Text","Image"],key="mode",label_visibility="collapsed")
    sel = st.selectbox("", list(PRESETS.keys()), label_visibility="collapsed", placeholder="Presets")
    if st.button("Use", use_container_width=True):
        st.session_state.preset_prompt = PRESETS[sel]
    up = st.file_uploader("", type=["png","jpg","jpeg","webp","txt","pdf"], label_visibility="collapsed")
    if up:
        p = GENERATED_DIR / f"up_{uuid.uuid4().hex}_{up.name}"
        p.write_bytes(up.getvalue())
        st.image(str(p), width=150) if up.type.startswith("image") else st.success(up.name)

for i,m in enumerate(st.session_state.messages):
    with st.container(border=True):
        if m["role"]=="user": st.code(m["content"])
        elif m["type"]=="text": st.code(m["content"]); copy_button(m["content"],i)
        elif m["type"]=="image" and os.path.exists(m["path"]): st.image(m["path"],use_container_width=True)

with st.form("f",clear_on_submit=True):
    q=st.text_input("", value=st.session_state.preset_prompt, placeholder="", label_visibility="collapsed")
    go=st.form_submit_button("Send",use_container_width=True)

if go and q.strip():
    q=q.strip()
    st.session_state.preset_prompt=""
    st.session_state.messages.append({"role":"user","type":"text","content":q})
    mode=st.session_state.mode
    if mode in ["Both","Text"]:
        try:
            with st.spinner(""): ans=generate_text(q)
            st.session_state.messages.append({"role":"assistant","type":"text","content":ans})
        except Exception as e: st.error(str(e))
    if mode in ["Both","Image"]:
        try:
            with st.spinner(""): ip=generate_image(q)
            st.session_state.messages.append({"role":"assistant","type":"image","path":ip})
        except Exception as e: st.error(str(e))
    st.rerun()
