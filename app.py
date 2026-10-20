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
IMAGE_API_URL = "https://gen.pollinations.ai/image/"
TEXT_API_URL = "https://text.pollinations.ai/"

st.set_page_config(page_title="Indian AI", layout="centered")

def copy_button(text, key):
    encoded_text = base64.b64encode(text.encode("utf-8")).decode("ascii")
    safe_key = "".join(c for c in str(key) if c.isalnum() or c in "_-")
    components.html(
        f"""
        <button id="copy_{safe_key}" style="background:#000;color:#fff;border:1px solid #fff;border-radius:8px;padding:8px 16px;cursor:pointer;">📋 Copy</button>
        <script>
        const btn=document.getElementById("copy_{safe_key}");
        btn.addEventListener("click", async function(){{
            const enc="{encoded_text}"; const bin=atob(enc);
            const bytes=Uint8Array.from(bin,c=>c.charCodeAt(0));
            const txt=new TextDecoder().decode(bytes);
            try{{await navigator.clipboard.writeText(txt); btn.innerText="✓ Copied!";}}
            catch(e){{btn.innerText="Failed";}}
        }});
        </script>
        """,
        height=48,
    )

# ================= BLACK + COLORFUL INDIA.JPG =================
background_css = ""
background_path = STATIC_DIR / "india.jpg"
if background_path.exists():
    encoded = base64.b64encode(background_path.read_bytes()).decode("ascii")
    suffix = background_path.suffix.lower()
    img_type = "image/png" if suffix == ".png" else "image/webp" if suffix == ".webp" else "image/jpeg"
    background_css = f'background-image: url("data:{img_type};base64,{encoded}"); background-size: cover; background-position: center; background-attachment: fixed; background-color: #000;'
else:
    background_css = "background-color: #000 !important;"

st.markdown(
    f"""
    <style>
    .stApp {{
        {background_css}
    }}
    /* Light overlay to keep india.jpg colorful */
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.35);
        z-index: -1;
    }}

    /* ===== ALL TEXT WHITE ===== */
    h1, h2, h3, h4, p, label, span, div {{
        color: #fff !important;
    }}
    h1 {{ text-align: center; }}

    /* ===== ALL BOXES BLACK + WHITE TEXT ===== */
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {{
        background: #000 !important;
        color: #fff !important;
        -webkit-text-fill-color: #fff !important;
        border: 1px solid #fff !important;
        border-radius: 10px !important;
    }}
    div[data-testid="stTextInput"] input::placeholder {{
        color: #aaa !important;
        -webkit-text-fill-color: #aaa !important;
    }}

    /* Chat containers - BLACK */
    div[data-testid="stChatMessage"],
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stContainer"] {{
        background: #000 !important;
        color: #fff !important;
        border: 1px solid #555 !important;
        border-radius: 10px !important;
    }}

    /* Code boxes - BLACK BOX WHITE TEXT */
    div[data-testid="stCode"],
    div[data-testid="stCode"] pre,
    div[data-testid="stCode"] code {{
        background: #000 !important;
        color: #fff !important;
        border: 1px solid #666 !important;
    }}

    /* Buttons - BLACK BOX WHITE TEXT */
    .stButton button,
    .stDownloadButton button,
    div[data-testid="stFormSubmitButton"] button,
    [data-testid="stPopover"] button {{
        background: #000 !important;
        color: #fff !important;
        border: 1px solid #fff !important;
        border-radius: 8px !important;
    }}
    .stButton button:hover,
    .stDownloadButton button:hover,
    div[data-testid="stFormSubmitButton"] button:hover {{
        background: #111 !important;
        border: 1px solid #fff !important;
        color: #fff !important;
    }}

    /* Popover body BLACK */
    div[data-testid="stPopoverBody"] {{
        background: #000 !important;
        color: #fff !important;
        border: 1px solid #fff !important;
    }}

    /* Selectbox BLACK */
    div[data-baseweb="select"] > div {{
        background: #000 !important;
        color: #fff !important;
        border-color: #fff !important;
    }}

    /* Spinner and alerts */
    div[data-testid="stSpinner"] {{
        color: #fff !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "Text"

def generate_text(prompt):
    try:
        r = requests.get(f"{TEXT_API_URL}{quote(prompt)}", timeout=60)
        if r.status_code == 200 and r.text.strip():
            return r.text.strip()
    except:
        pass
    raise RuntimeError("Text generation failed")

def generate_image(prompt):
    headers = {}
    if POLLINATIONS_API_KEY:
        headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"
    r = requests.get(
        IMAGE_API_URL + quote(prompt, safe=""),
        params={{"model": "flux", "width": 1024, "height": 1024}},
        headers=headers,
        timeout=240,
    )
    if r.status_code != 200:
        raise RuntimeError(f"Image error {r.status_code}")
    ext = ".jpg"
    if "png" in r.headers.get("Content-Type",""):
        ext = ".png"
    p = GENERATED_DIR / f"image_{{uuid.uuid4().hex}}{{ext}}"
    p.write_bytes(r.content)
    return str(p)

st.title("Indian AI")
st.caption("Ask questions or generate images")

with st.popover("＋ Tools and attachments"):
    st.selectbox("Choose mode", ["Text", "Image", "Both"], key="mode")

for idx, msg in enumerate(st.session_state.messages):
    with st.container(border=True):
        if msg["role"] == "user":
            st.markdown("**You**")
            st.code(msg["content"], language=None)
        elif msg["type"] == "text":
            st.markdown("**Indian AI**")
            st.code(msg["content"], language=None)
            copy_button(msg["content"], f"resp_{{idx}}")
            st.download_button(
                "⬇ Download response",
                data=msg["content"],
                file_name="response.txt",
                mime="text/plain",
                key=f"txt_{{idx}}",
            )
        elif msg["type"] == "image":
            st.markdown("**Indian AI — Generated Image**")
            path = msg["path"]
            if os.path.exists(path):
                st.image(path, use_container_width=True)
                with open(path, "rb") as f:
                    st.download_button(
                        "⬇ Download image",
                        data=f.read(),
                        file_name=Path(path).name,
                        key=f"img_{{idx}}",
                    )

with st.form("prompt_form", clear_on_submit=True):
    prompt = st.text_input(
        "Message Indian AI",
        placeholder="Ask a question or describe an image...",
        label_visibility="collapsed",
    )
    send = st.form_submit_button("➤ Send", use_container_width=True)

if send and prompt.strip():
    prompt = prompt.strip()
    st.session_state.messages.append(
        {{"role": "user", "type": "text", "content": prompt}}
    )
    mode = st.session_state.mode
    if mode in ["Text", "Both"]:
        try:
            with st.spinner("Generating text..."):
                ans = generate_text(prompt)
            st.session_state.messages.append(
                {{"role": "assistant", "type": "text", "content": ans}}
            )
        except Exception as e:
            st.error(f"Text failed: {{e}}")
    if mode in ["Image", "Both"]:
        try:
            with st.spinner("Generating image..."):
                img_path = generate_image(prompt)
            st.session_state.messages.append(
                {{"role": "assistant", "type": "image", "path": img_path}}
            )
        except Exception as e:
            st.error(f"Image failed: {{e}}")
    st.rerun()
