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

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "").strip()
TEXT_API_URL = "https://text.pollinations.ai/"

st.set_page_config(page_title="Indian AI", layout="centered")

def copy_button(text, key):
    encoded_text = base64.b64encode(text.encode("utf-8")).decode("ascii")
    safe_key = "".join(c for c in str(key) if c.isalnum() or c in "_-")
    components.html(
        f"""<button id="copy_{safe_key}" style="background:#000;color:#fff;border:1px solid #fff;border-radius:8px;padding:8px 16px;cursor:pointer;">Copy</button>
        <script>const b=document.getElementById("copy_{safe_key}");b.addEventListener("click",async function(){{const e="{encoded_text}";const bin=atob(e);const bytes=Uint8Array.from(bin,c=>c.charCodeAt(0));const t=new TextDecoder().decode(bytes);try{{await navigator.clipboard.writeText(t);b.innerText="Copied!";}}catch(e){{b.innerText="Failed";}}}});</script>""",
        height=48,
    )

# BACKGROUND BLACK + COLORFUL
bp = STATIC_DIR / "india.jpg"
if bp.exists():
    enc = base64.b64encode(bp.read_bytes()).decode("ascii")
    bg_css = f'background-image: url("data:image/jpeg;base64,{enc}"); background-size: cover; background-position: center; background-attachment: fixed; background-color:#000;'
else:
    bg_css = "background-color:#000 !important;"

st.markdown(f"""<style>.stApp{{{bg_css}}} .stApp::before{{content:"";position:fixed;inset:0;background:rgba(0,0,0,0.35);z-index:-1;}} h1, p, label{{color:#fff !important;}} h1{{text-align:center;}} div[data-testid="stTextInput"] input{{background:#000 !important;color:#fff !important;border:1px solid #fff !important;border-radius:10px !important;}} div[data-testid="stVerticalBlockBorderWrapper"]{{background:#000 !important;border:1px solid #555 !important;}} div[data-testid="stCode"], div[data-testid="stCode"] pre{{background:#000 !important;color:#fff !important;border:1px solid #666 !important;}} .stButton button, .stDownloadButton button, div[data-testid="stFormSubmitButton"] button{{background:#000 !important;color:#fff !important;border:1px solid #fff !important;}}</style>""", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
if "mode" not in st.session_state: st.session_state.mode = "Both"

def generate_text(prompt):
    r = requests.get(f"{TEXT_API_URL}{quote(prompt)}", timeout=90)
    if r.status_code == 200 and r.text.strip():
        return r.text.strip()
    raise RuntimeError("Text failed")

def generate_image(prompt):
    # TRY 1: New Pollinations Image API (works without key)
    try:
        url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width=1024&height=1024&model=flux&nologo=true"
        r = requests.get(url, timeout=120)
        if r.status_code == 200 and r.content:
            if b"html" not in r.content[:100].lower():
                p = GENERATED_DIR / f"image_{uuid.uuid4().hex}.jpg"
                p.write_bytes(r.content)
                return str(p)
    except Exception as e:
        print(f"Try1 failed: {e}")

    # TRY 2: Old gen API with/without key
    try:
        headers = {}
        if POLLINATIONS_API_KEY:
            headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"
        url2 = f"https://gen.pollinations.ai/image/{quote(prompt)}"
        r2 = requests.get(url2, params={"width":1024,"height":1024,"model":"flux"}, headers=headers, timeout=120)
        if r2.status_code == 200 and r2.content:
            p = GENERATED_DIR / f"image_{uuid.uuid4().hex}.jpg"
            p.write_bytes(r2.content)
            return str(p)
        else:
            raise RuntimeError(f"API {r2.status_code}: {r2.text[:300]}")
    except Exception as e:
        raise RuntimeError(f"Image generation failed: {e}")

st.title("Indian AI")
st.caption("Both Text + Image")
with st.popover("＋ Tools"): st.selectbox("Choose mode", ["Both","Text","Image"], key="mode")

for idx, msg in enumerate(st.session_state.messages):
    with st.container(border=True):
        if msg["role"] == "user":
            st.markdown("**You**"); st.code(msg["content"])
        elif msg["type"] == "text":
            st.markdown("**Indian AI**"); st.code(msg["content"]); copy_button(msg["content"], f"r_{idx}")
        elif msg["type"] == "image":
            path = msg["path"]
            if os.path.exists(path):
                st.markdown("**Indian AI — Image**")
                st.image(path, use_container_width=True)
                with open(path, "rb") as f:
                    st.download_button("⬇ Download image", f.read(), file_name=Path(path).name, key=f"img_{idx}")

with st.form("prompt_form", clear_on_submit=True):
    p = st.text_input("Message Indian AI", placeholder="Describe image or ask question...", label_visibility="collapsed")
    send = st.form_submit_button("➤ Send Both", use_container_width=True)

if send and p.strip():
    p = p.strip()
    st.session_state.messages.append({"role":"user","type":"text","content":p})
    mode = st.session_state.mode

    if mode in ["Both","Text"]:
        try:
            with st.spinner("Generating text..."): ans = generate_text(p)
            st.session_state.messages.append({"role":"assistant","type":"text","content":ans})
        except Exception as e: st.error(f"Text failed: {e}")

    if mode in ["Both","Image"]:
        try:
            with st.spinner("Generating image... This takes 10-20 sec"):
                img_path = generate_image(p)
            st.session_state.messages.append({"role":"assistant","type":"image","path":img_path})
        except Exception as e: st.error(str(e))

    st.rerun()
