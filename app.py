import os
import uuid
import base64
from pathlib import Path
from urllib.parse import quote

import requests
import streamlit as st
import streamlit.components.v1 as components

# Make dotenv optional — won't crash on Streamlit Cloud
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# ================= CONFIGURATION =================
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
GENERATED_DIR = STATIC_DIR / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "").strip()
IMAGE_API_URL = "https://gen.pollinations.ai/image/"
TEXT_API_URL = "https://text.pollinations.ai/"

st.set_page_config(page_title="Indian AI", layout="centered")

# ================= COPY BUTTON =================
def copy_button(text, key):
    encoded_text = base64.b64encode(text.encode("utf-8")).decode("ascii")
    safe_key = "".join(char for char in str(key) if char.isalnum() or char in "_-")
    components.html(
        f"""
        <button id="copy_{safe_key}" style="background:#000;color:#fff;border:1px solid #666;border-radius:8px;padding:8px 16px;cursor:pointer;">📋 Copy</button>
        <script>
        const button = document.getElementById("copy_{safe_key}");
        button.addEventListener("click", async function() {{
            const encoded = "{encoded_text}";
            const binary = atob(encoded);
            const bytes = Uint8Array.from(binary, c => c.charCodeAt(0));
            const text = new TextDecoder().decode(bytes);
            try {{ await navigator.clipboard.writeText(text); button.innerText = "✓ Copied!"; }}
            catch (error) {{
                const area = document.createElement("textarea"); area.value = text;
                area.style.position = "fixed"; area.style.left = "-9999px";
                document.body.appendChild(area); area.focus(); area.select();
                try {{ const success = document.execCommand("copy"); button.innerText = success ? "✓ Copied!" : "Copy failed"; }}
                catch (e) {{ button.innerText = "Copy failed"; }} area.remove();
            }}
        }});
        </script>
        """, height=48,
    )

# ================= BACKGROUND =================
background_css = ""
background_path = STATIC_DIR / "india.jpg"
if background_path.exists():
    encoded_background = base64.b64encode(background_path.read_bytes()).decode("ascii")
    suffix = background_path.suffix.lower()
    image_type = "image/png" if suffix == ".png" else "image/webp" if suffix == ".webp" else "image/jpeg"
    background_css = f"""background-image: linear-gradient(rgba(0,0,0,0.76), rgba(0,0,0,0.88)), url("data:{image_type};base64,{encoded_background}"); background-size:cover; background-position:center; background-attachment:fixed;"""
st.markdown(f"""<style>.stApp {{{background_css} background-color:#000 !important; color:#fff !important;}} h1 {{text-align:center; color:#fff !important;}} h2, h3, p, label {{color:#fff !important;}} div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {{background:#000 !important; color:#fff !important; -webkit-text-fill-color:#fff !important; border:1px solid #666 !important; border-radius:10px !important;}} .stButton button, .stDownloadButton button, div[data-testid="stFormSubmitButton"] button, [data-testid="stPopover"] button {{background:#000 !important; color:#fff !important; border:1px solid #666 !important; border-radius:9px !important;}}</style>""", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
if "mode" not in st.session_state: st.session_state.mode = "Text"

# ================= TEXT GENERATION - FIXED FOR CLOUD =================
def generate_text(prompt):
    # Uses Pollinations text API — works on cloud, no localhost needed
    try:
        resp = requests.post(TEXT_API_URL, json={"messages": [{"role": "user", "content": prompt}], "model": "openai", "seed": -1}, timeout=60)
        if resp.status_code == 200 and resp.text.strip():
            return resp.text.strip()
    except: pass
    # Fallback GET
    try:
        resp = requests.get(f"{TEXT_API_URL}{quote(prompt)}", timeout=60)
        if resp.status_code == 200 and resp.text.strip():
            return resp.text.strip()
    except Exception as e: pass
    raise RuntimeError("Text generation failed. Check internet or try again.")

def generate_image(prompt):
    headers = {}
    if POLLINATIONS_API_KEY: headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"
    response = requests.get(IMAGE_API_URL + quote(prompt, safe=""), params={"model": "black-forest-labs/flux.1-schnell", "width": 1024, "height": 1024}, headers=headers, timeout=240)
    if response.status_code != 200: raise RuntimeError(f"Image API error {response.status_code}: {response.text[:400]}")
    content_type = response.headers.get("Content-Type", "").lower()
    if not content_type.startswith("image/"): raise RuntimeError(f"Did not return image: {content_type}")
    extension = ".png" if "png" in content_type else ".webp" if "webp" in content_type else ".jpg"
    image_path = GENERATED_DIR / f"image_{uuid.uuid4().hex}{extension}"
    image_path.write_bytes(response.content)
    return str(image_path)

st.title("Indian AI")
st.caption("Ask questions or generate images from your prompts.")
with st.popover("＋ Tools and attachments"): st.selectbox("Choose mode", ["Text", "Image", "Both"], key="mode")
for index, message in enumerate(st.session_state.messages):
    with st.container(border=True):
        if message["role"] == "user": st.markdown("**You**"); st.code(message["content"], language=None)
        elif message["type"] == "text": st.markdown("**Indian AI**"); st.code(message["content"], language=None); copy_button(message["content"], f"response_{index}"); st.download_button("⬇ Download response", data=message["content"], file_name="indian_ai_response.txt", mime="text/plain", key=f"download_text_{index}")
        elif message["type"] == "image": st.markdown("**Indian AI — Generated Image**"); image_path = message["path"]; 
                if os.path.exists(image_path): st.image(image_path, use_container_width=True); 
                with open(image_path, "rb") as image_file: image_data = image_file.read(); st.download_button("⬇ Download image", data=image_data, file_name=Path(image_path).name, mime="application/octet-stream", key=f"download_image_{index}")

with st.form("prompt_form", clear_on_submit=True):
    prompt = st.text_input("Message Indian AI", placeholder="Ask a question or describe an image...", label_visibility="collapsed")
    send = st.form_submit_button("➤ Send", use_container_width=True)

if send and prompt.strip():
    prompt = prompt.strip()
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    mode = st.session_state.mode
    if mode in ["Text", "Both"]:
        try:
            with st.spinner("Generating text response..."): answer = generate_text(prompt)
            st.session_state.messages.append({"role": "assistant", "type": "text", "content": answer})
        except Exception as error: st.error(f"Text generation failed: {error}")
    if mode in ["Image", "Both"]:
        try:
            with st.spinner("Generating your image..."): image_path = generate_image(prompt)
            st.session_state.messages.append({"role": "assistant", "type": "image", "path": image_path})
        except Exception as error: st.error(f"Image generation failed: {error}")
    st.rerun()
