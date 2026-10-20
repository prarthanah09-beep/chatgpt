
import os
import uuid
import base64
from pathlib import Path
from urllib.parse import quote

import requests
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

load_dotenv()

# ================= CONFIGURATION =================

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
GENERATED_DIR = STATIC_DIR / "generated"

GENERATED_DIR.mkdir(parents=True, exist_ok=True)

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2:3b"

POLLINATIONS_API_KEY = os.getenv(
    "POLLINATIONS_API_KEY", ""
).strip()

IMAGE_API_URL = "https://gen.pollinations.ai/image/"

st.set_page_config(
    page_title="Indian AI",
    layout="centered",
)

# ================= COPY BUTTON =================

def copy_button(text, key):
    encoded_text = base64.b64encode(
        text.encode("utf-8")
    ).decode("ascii")

    # Keep the HTML element ID safe and unique.
    safe_key = "".join(
        char for char in str(key)
        if char.isalnum() or char in "_-"
    )

    components.html(
        f"""
        <button id="copy_{safe_key}" style="
            background:#000;
            color:#fff;
            border:1px solid #666;
            border-radius:8px;
            padding:8px 16px;
            cursor:pointer;
            font-size:14px;
        ">📋 Copy</button>

        <script>
        const button =
            document.getElementById("copy_{safe_key}");

        button.addEventListener("click", async function() {{
            const encoded = "{encoded_text}";
            const binary = atob(encoded);
            const bytes = Uint8Array.from(
                binary, c => c.charCodeAt(0)
            );
            const text = new TextDecoder().decode(bytes);

            try {{
                await navigator.clipboard.writeText(text);
                button.innerText = "✓ Copied!";
            }} catch (error) {{
                const area = document.createElement("textarea");
                area.value = text;
                area.style.position = "fixed";
                area.style.left = "-9999px";
                document.body.appendChild(area);
                area.focus();
                area.select();

                try {{
                    const success =
                        document.execCommand("copy");

                    button.innerText = success
                        ? "✓ Copied!"
                        : "Copy failed";
                }} catch (e) {{
                    button.innerText = "Copy failed";
                }}

                area.remove();
            }}
        }});
        </script>
        """,
        height=48,
    )


# ================= BACKGROUND =================

background_css = ""
background_path = STATIC_DIR / "india.jpg"

if background_path.exists():
    encoded_background = base64.b64encode(
        background_path.read_bytes()
    ).decode("ascii")

    suffix = background_path.suffix.lower()

    if suffix == ".png":
        image_type = "image/png"
    elif suffix == ".webp":
        image_type = "image/webp"
    else:
        image_type = "image/jpeg"

    background_css = f"""
        background-image:
            linear-gradient(
                rgba(0,0,0,0.76),
                rgba(0,0,0,0.88)
            ),
            url("data:{image_type};base64,{encoded_background}");
        background-size:cover;
        background-position:center;
        background-attachment:fixed;
    """

st.markdown(
    f"""
    <style>
    .stApp {{
        {background_css}
        background-color:#000 !important;
        color:#fff !important;
    }}

    h1 {{
        text-align:center;
        color:#fff !important;
    }}

    h2, h3, p, label {{
        color:#fff !important;
    }}

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {{
        background:#000 !important;
        color:#fff !important;
        -webkit-text-fill-color:#fff !important;
        border:1px solid #666 !important;
        border-radius:10px !important;
    }}

    div[data-testid="stTextInput"] input::placeholder {{
        color:#aaa !important;
        -webkit-text-fill-color:#aaa !important;
    }}

    .stButton button,
    .stDownloadButton button,
    div[data-testid="stFormSubmitButton"] button,
    [data-testid="stPopover"] button {{
        background:#000 !important;
        color:#fff !important;
        border:1px solid #666 !important;
        border-radius:9px !important;
    }}

    .stButton button:hover,
    .stDownloadButton button:hover,
    div[data-testid="stFormSubmitButton"] button:hover {{
        background:#222 !important;
        color:#fff !important;
        border:1px solid #fff !important;
    }}

    div[data-testid="stCode"],
    div[data-testid="stCode"] pre,
    div[data-testid="stCode"] code {{
        background:#000 !important;
        color:#fff !important;
        border:1px solid #444 !important;
    }}

    div[data-testid="stPopoverBody"] {{
        background:#000 !important;
        color:#fff !important;
    }}

    div[data-testid="stChatMessage"] {{
        background:#000 !important;
        color:#fff !important;
        border:1px solid #444 !important;
        border-radius:10px !important;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# ================= SESSION STATE =================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "Text"

# ================= TEXT GENERATION =================

def generate_text(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
        },
        timeout=180,
    )

    response.raise_for_status()

    answer = response.json().get(
        "message", {}
    ).get("content", "").strip()

    if not answer:
        raise RuntimeError(
            "The text model returned an empty response."
        )

    return answer

# ================= IMAGE GENERATION =================

def generate_image(prompt):
    if not POLLINATIONS_API_KEY:
        raise RuntimeError(
            "Missing Pollinations API key. Add "
            "POLLINATIONS_API_KEY to your .env file."
        )

    response = requests.get(
        IMAGE_API_URL + quote(prompt, safe=""),
        params={
            "model": "black-forest-labs/flux.1-schnell",
            "width": 1024,
            "height": 1024,
        },
        headers={
            "Authorization":
                f"Bearer {POLLINATIONS_API_KEY}"
        },
        timeout=240,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Image API error {response.status_code}: "
            f"{response.text[:400]}"
        )

    content_type = response.headers.get(
        "Content-Type", ""
    ).lower()

    if not content_type.startswith("image/"):
        raise RuntimeError(
            "The image service did not return an image. "
            f"Received: {content_type or 'unknown content'}"
        )

    if "png" in content_type:
        extension = ".png"
    elif "webp" in content_type:
        extension = ".webp"
    else:
        extension = ".jpg"

    image_path = GENERATED_DIR / (
        f"image_{uuid.uuid4().hex}{extension}"
    )

    image_path.write_bytes(response.content)

    return str(image_path)

# ================= HEADER =================

st.title("Indian AI")
st.caption("Ask questions or generate images from your prompts.")

# ================= TOOLS =================

with st.popover("＋ Tools and attachments"):
    st.selectbox(
        "Choose mode",
        ["Text", "Image", "Both"],
        key="mode",
    )

# ================= CHAT HISTORY =================

for index, message in enumerate(st.session_state.messages):

    with st.container(border=True):

        if message["role"] == "user":
            st.markdown("**You**")
            st.code(
                message["content"],
                language=None,
            )

        elif message["type"] == "text":
            st.markdown("**Indian AI**")

            # Black response box with white text.
            st.code(
                message["content"],
                language=None,
            )

            # Separate visible Copy button.
            copy_button(
                message["content"],
                f"response_{index}",
            )

            st.download_button(
                "⬇ Download response",
                data=message["content"],
                file_name="indian_ai_response.txt",
                mime="text/plain",
                key=f"download_text_{index}",
            )

        elif message["type"] == "image":
            st.markdown("**Indian AI — Generated Image**")

            image_path = message["path"]

            if os.path.exists(image_path):
                st.image(
                    image_path,
                    use_container_width=True,
                )

                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()

                st.download_button(
                    "⬇ Download image",
                    data=image_data,
                    file_name=Path(image_path).name,
                    mime="application/octet-stream",
                    key=f"download_image_{index}",
                )

# ================= INPUT BOX =================

with st.form("prompt_form", clear_on_submit=True):

    prompt = st.text_input(
        "Message Indian AI",
        placeholder="Ask a question or describe an image...",
        label_visibility="collapsed",
    )

    send = st.form_submit_button(
        "➤ Send",
        use_container_width=True,
    )

# ================= PROCESS REQUEST =================

if send and prompt.strip():

    prompt = prompt.strip()

    st.session_state.messages.append({
        "role": "user",
        "type": "text",
        "content": prompt,
    })

    mode = st.session_state.mode

    if mode == "Text":

        try:
            with st.spinner("Generating text response..."):
                answer = generate_text(prompt)

            st.session_state.messages.append({
                "role": "assistant",
                "type": "text",
                "content": answer,
            })

        except Exception as error:
            st.error(f"Text generation failed: {error}")

    elif mode == "Image":

        try:
            with st.spinner("Generating your image..."):
                image_path = generate_image(prompt)

            st.session_state.messages.append({
                "role": "assistant",
                "type": "image",
                "path": image_path,
            })

        except Exception as error:
            st.error(f"Image generation failed: {error}")

    elif mode == "Both":

        try:
            with st.spinner("Generating text response..."):
                answer = generate_text(prompt)

            st.session_state.messages.append({
                "role": "assistant",
                "type": "text",
                "content": answer,
            })

        except Exception as error:
            st.error(f"Text generation failed: {error}")

        try:
            with st.spinner("Generating your image..."):
                image_path = generate_image(prompt)

            st.session_state.messages.append({
                "role": "assistant",
                "type": "image",
                "path": image_path,
            })

        except Exception as error:
            st.error(f"Image generation failed: {error}")

    st.rerun()
