import os, uuid, base64
from pathlib import Path
from urllib.parse import quote
import requests
import streamlit as st
import streamlit.components.v1 as components

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
GENERATED_DIR = STATIC_DIR / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)
API_KEY = os.getenv("POLLINATIONS_API_KEY", "").strip()

st.set_page_config(page_title="Indian AI", layout="centered")

def copy_btn(text, key):
    enc = base64.b64encode(text.encode("utf-8")).decode("ascii")
    safe = "".join(c for c in str(key) if c.isalnum() or c in "_-")
    components.html(f"""<button id="b_{safe}" style="background:#000;color:#fff;border:1px solid #fff;border-radius:8px;padding:6px 14px">Copy</button>
    <script>const x=document.getElementById("b_{safe}");x.onclick=async()=>{{let e="{enc}";let b=atob(e);let u=Uint8Array.from(b,c=>c.charCodeAt(0));let t=new TextDecoder().decode(u);await navigator.clipboard.writeText(t);x.innerText="Copied!"}}</script>""", height=45)

bp = STATIC_DIR / "india.jpg"
if bp.exists():
    b64 = base64.b64encode(bp.read_bytes()).decode()
    bg = f'background-image:url("data:image/jpeg;base64,{b64}");background-size:cover;background-position:center;background-attachment:fixed;background-color:#000;'
else:
    bg = "background:#000!important;"

st.markdown(f"""
<style>
.stApp {{ {bg} }}
.stApp::before {{ content:""; position:fixed; inset:0; background:rgba(0,0,0,0.4); z-index:-1; }}
html, body, h1, h2, h3, p, span, label, div, li {{ color:#fff !important; }}
h1 {{ text-align:center; }}
input, textarea, [data-testid="stTextInput"] input {{
    background:#000 !important; color:#fff !important; -webkit-text-fill-color:#fff !important;
    border:1px solid #fff !important; border-radius:10px !important;
}}
[data-testid="stVerticalBlockBorderWrapper"], [data-testid="stContainer"], [data-testid="stChatMessage"], [data-testid="stForm"], [data-testid="stPopoverBody"] {{
    background:#000 !important; border:1px solid #777 !important; border-radius:12px !important;
}}
div[data-baseweb="select"], div[data-baseweb="select"] > div, div[role="listbox"], ul[role="listbox"] {{
    background:#000 !important; color:#fff !important; border-color:#fff !important;
}}
li[role="option"] {{ background:#000 !important; color:#fff !important; }}
[data-testid="stCode"], [data-testid="stCode"] pre {{
    background:#000 !important; color:#fff !important; border:1px solid #555 !important;
}}
button, .stButton button, .stDownloadButton button, [data-testid="stFormSubmitButton"] button {{
    background:#000 !important; color:#fff !important; border:1px solid #fff !important;
}}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "Both"

def gen_text(p):
    r = requests.get(f"https://text.pollinations.ai/{quote(p)}", timeout=90)
    if r.status_code == 200 and r.text.strip():
        return r.text.strip()
    raise RuntimeError("Text failed")

def gen_image(p):
    hdr = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
    urls = [
        f"https://image.pollinations.ai/prompt/{quote(p)}?width=1024&height=1024&model=flux&nologo=true",
        f"https://gen.pollinations.ai/image/{quote(p)}"
    ]
    for url in urls:
        try:
            resp = requests.get(url, params={"width": 1024, "height": 1024, "model": "flux"}, headers=hdr, timeout=120)
            if resp.status_code == 200 and len(resp.content) > 5000:
                fp = GENERATED_DIR / f"img_{uuid.uuid4().hex}.jpg"
                fp.write_bytes(resp.content)
                return str(fp)
        except:
            continue
    raise RuntimeError("Image failed")

st.title("Indian AI")

with st.popover("Tools"):
    st.selectbox("Mode", ["Both", "Text", "Image"], key="mode")

for i, msg in enumerate(st.session_state.messages):
    with st.container(border=True):
        if msg["role"] == "user":
            st.markdown("**You**")
            st.code(msg["content"])
        elif msg["type"] == "text":
            st.markdown("**Indian AI**")
            st.code(msg["content"])
            copy_btn(msg["content"], i)
        elif msg["type"] == "image":
            if os.path.exists(msg["path"]):
                st.markdown("**Indian AI**")
                st.image(msg["path"], use_container_width=True)
                with open(msg["path"], "rb") as f:
                    st.download_button("Download", f.read(), file_name=Path(msg["path"]).name, key=f"dl{i}")

with st.form("f", clear_on_submit=True):
    q = st.text_input("msg", placeholder="Ask anything...", label_visibility="collapsed")
    go = st.form_submit_button("Send", use_container_width=True)

if go and q.strip():
    q = q.strip()
    st.session_state.messages.append({"role": "user", "type": "text", "content": q})
    m = st.session_state.mode
    if m in ["Both", "Text"]:
        try:
            with st.spinner("Generating..."):
                ans = gen_text(q)
            st.session_state.messages.append({"role": "assistant", "type": "text", "content": ans})
        except Exception as e:
            st.error(str(e))
    if m in ["Both", "Image"]:
        try:
            with st.spinner("Creating image..."):
                ip = gen_image(q)
            st.session_state.messages.append({"role": "assistant", "type": "image", "path": ip})
        except Exception as e:
            st.error(str(e))
    st.rerun()
