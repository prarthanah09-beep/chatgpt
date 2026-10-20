import os
import uuid
import base64
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

def copy_button(text, key):
    enc = base64.b64encode(text.encode("utf-8")).decode("ascii")
    safe = "".join(c for c in str(key) if c.isalnum() or c in "_-")
    components.html(
        f"""<button id="c_{safe}" style="background:#000;color:#fff;border:1px solid #fff;border-radius:8px;padding:8px 16px;cursor:pointer;">Copy</button>
        <script>const b=document.getElementById("c_{safe}");b.addEventListener("click",async()=>{{const e="{enc}";const bin=atob(e);const bytes=Uint8Array.from(bin,c=>c.charCodeAt(0));const t=new TextDecoder().decode(bytes);try{{await navigator.clipboard.writeText(t);b.innerText="Copied!";}}catch{{b.innerText="Failed";}}}});</script>""",
        height=48,
    )

# BLACK BG + COLORFUL india.jpg
bp = STATIC_DIR / "india.jpg"
if bp.exists():
    b64 = base64.b64encode(bp.read_bytes()).decode("ascii")
    bg = f'background-image: url("data:image/jpeg;base64,{b64}"); background-size: cover; background-position: center; background-attachment: fixed; background-color: #000;'
else:
    bg = "background-color: #000 !important;"

st.markdown(f"""
<style>
.stApp {{ {bg} }}
.stApp::before {{ content:""; position:fixed; inset:0; background:rgba(0,0,0,0.35); z-index:-1; }}
h1,h2,h3,p,label,span,div,li {{ color:#fff !important; }} 
h1 {{ text-align:center; }}
div[data-testid="stTextInput"] input {{
    background:#000 !important; color:#fff !important; -webkit-text-fill-color:#fff !important;
    border:1px solid #fff !important; border-radius:10px !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stContainer"], div[data-testid="stChatMessage"] {{
    background:#000 !important; color:#fff !important; border:1px solid #666 !important; border-radius:12px !important;
}}
div[data-testid="stCode"], div[data-testid="stCode"] pre, div[data-testid="stCode"] code {{
    background:#000 !important; color:#fff !important; border:1px solid #555 !important;
}}
.stButton button, .stDownloadButton button, div[data-testid="stFormSubmitButton"] button, [data-testid="stPopover"] button {{
    background:#000 !important; color:#fff !important; border:1px solid #fff !important; border-radius:8px !important;
}}
div[data-testid="stPopoverBody"] {{ background:#000 !important; border:1px solid #fff !important; }}
div[data-baseweb="select"] > div {{ background:#000 !important; color:#fff !important; }}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
if "mode" not in st.session_state: st.session_state.mode = "Both"

def generate_text(prompt):
    r = requests.get(f"https://text.pollinations.ai/{quote(prompt)}", timeout=90)
    if r.status_code == 200 and r.text.strip():
        return r.text.strip()
    raise RuntimeError("Failed to generate response")

def generate_image(prompt):
    headers = {}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    # Free endpoint first, then pro endpoint
    for url in [
        f"https://image.pollinations.ai/prompt/{quote(prompt)}?width=1024&height=1024&model=flux&nologo=true",
        f"https://gen.pollinations.ai/image/{quote(prompt)}"
    ]:
        try:
            resp = requests.get(url, params={"width":1024,"height":1024,"model":"flux"}, headers=headers, timeout=120)
            if resp.status_code == 200 and len(resp.content) > 5000:
                path = GENERATED_DIR / f"img_{uuid.uuid4().hex}.jpg"
                path.write_bytes(resp.content)
                return str(path)
        except:
            continue
    raise RuntimeError("Image generation failed. Try again")

st.title("Indian AI")
st.caption("Text and Image generation")

with st.popover("Tools"): st.selectbox("Mode", ["Both","Text","Image"], key="mode")

for idx, msg in enumerate(st.session_state.messages):
    with st.container(border=True):
        if msg["role"] == "user":
            st.markdown("**You**")
            st.code(msg["content"])
        elif msg["type"] == "text":
            st.markdown("**Indian AI**")
            st.code(msg["content"])
            copy_button(msg["content"], f"t{idx}")
        elif msg["type"] == "image":
            if os.path.exists(msg["path"]):
                st.markdown("**Indian AI**")
                st.image(msg["path"], use_container_width=True)
                with open(msg["path"], "rb") as f:
                    st.download_button("Download image", f.read(), file_name=Path(msg["path"]).name, key=f"i{idx}")

with st.form("chat", clear_on_submit=True):
    q = st.text_input("Message", placeholder="Ask anything...", label_visibility="collapsed")
    go = st.form_submit_button("Send", use_container_width=True)

if go and q.strip():
    q = q.strip()
    st.session_state.messages.append({"role":"user","type":"text","content":q})
    m = st.session_state.mode

    if m in ["Both","Text"]:
        try:
            with st.spinner("Generating..."):
                ans = generate_text(q)
            st.session_state.messages.append({"role":"assistant","type":"text","content":ans})
        except Exception as e:
            st.error(f"{e}")

    if m in ["Both","Image"]:
        try:
            with st.spinner("Creating image..."):
                ip = generate_image(q)
            st.session_state.messages.append({"role":"assistant","type":"image","path":ip})
        except Exception as e:
            st.error(f"{e}")

    st.rerun()
