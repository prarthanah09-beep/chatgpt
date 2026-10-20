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
div[data-baseweb="select"],
