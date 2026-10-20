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

bp=STATIC_DIR/"india.jpg"
bg_css=f'background-image:linear-gradient(rgba(0,0,0,0.76),rgba(0,0,0,0.88)),url("data:image/jpeg;base64,{base64.b64encode(bp.read_bytes()).decode()}");background-size:cover;background-position:center;background-attachment:fixed;' if bp.exists() else ""

st.markdown(f"""
<style>
.stApp{{{bg_css}background:#000!important}}
h1,p,label,span,div,li{{color:#fff!important}} h1{{text-align:center}}
div[data-testid="stTextInput"] input{{background:#000!important;color:#fff!important;-webkit-text-fill-color:#fff!important;border:1px solid #666!important;border-radius:10px!important}}
div[data-testid="stVerticalBlockBorderWrapper"],div[data-testid="stContainer"],div[data-testid="stForm"],div[data-testid="stPopoverBody"],div[data-testid="stChatMessage"],div[data-testid="stFileUploader"]{{background:#000!important;border:1px solid #444!important;border-radius:12px!important}}
div[data-baseweb="select"],div[data-baseweb="select"]>div,div[role="listbox"],ul[role="listbox"]{{background:#000!important;color:#fff!important}}
li[role="option"]{{background:#000!important;color:#fff!important}}
div[data-testid="stCode"],div[data-testid="stCode"] pre{{background:#000!important;color:#fff!important;border:1px solid #444!important}}
.stButton button,.stDownloadButton button,div[data-testid="stFormSubmitButton"] button,[data-testid="stPopover"] button{{background:#000!important;color:#fff!important;border:1px solid #666!important}}
section[data-testid="stFileUploaderDropzone"]{{background:#000!important;border:1px dashed #666!important;color:#fff!important}}
</style>""",unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages=[]
if "mode" not in st.session_state: st.session_state.mode="Both"
if "preset_prompt" not in st.session_state: st.session_state.preset_prompt=""

def generate_text(p):
    r=requests.get(f"https://text.pollinations.ai/{quote(p)}",timeout=90)
    if r.status_code==200 and r.text.strip(): return r.text.strip()
    raise RuntimeError("Text failed")

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

# ALL PRESETS
PRESETS = {
"--- GHIBLI REAL FOOD ---": "",
"Spirited Away Buns": "Spirited Away steamed pork buns, photorealistic real food, fluffy baozi, steam rising, 8k food photography, black background",
"Howl's Breakfast": "Howl's Moving Castle breakfast, real fried eggs and bacon sizzling in cast iron pan, photorealistic, 8k",
"Ponyo Ramen": "Ponyo ramen, real ham ramen with boiled egg and green onions, steaming hot, photorealistic, ultra detailed",
"Totoro Bento": "My Neighbor Totoro bento box, real Japanese lunch box, photorealistic, studio lighting, 8k",

"--- OGGY REAL LIFE ---": "",
"Oggy Real Cat": "Oggy from Oggy and the Cockroaches, photorealistic real blue-grey fluffy cat standing like human wearing clothes, ultra detailed fur, 8k, black background",
"Oggy Cockroaches Real": "Dee Dee Joey Marky cockroaches from Oggy, photorealistic real cockroaches with big eyes standing like humans, funny, ultra detailed, 8k",
"Jack Real": "Jack from Oggy and the Cockroaches, photorealistic real olive green muscular cat, angry expression, real fur, 8k",

"--- TOM & JERRY REAL ---": "",
"Tom & Jerry Real Fight": "Tom and Jerry in real life, photorealistic grey cat and brown mouse fighting in kitchen, ultra detailed fur, National Geographic style, 8k",
"Tom Real Cat": "Tom the cat from Tom and Jerry, photorealistic real grey and white cat with yellow eyes, shocked expression, ultra detailed, 8k",
"Jerry Real Mouse": "Jerry the mouse from Tom and Jerry, photorealistic real cute brown mouse with big ears, smart expression, real fur texture, 8k",
"Spike Real Dog": "Spike the bulldog from Tom and Jerry, photorealistic real bulldog with spiked collar, angry, ultra detailed, 8k",

"--- CHOTA BHEEM & INDIAN ---": "",
"Chota Bheem Real Boy": "Chota Bheem in real life, photorealistic 9 year old Indian boy with dhoti, strong, bald with small tuft, laddoo in hand, Dholakpur, ultra detailed, 8k",
"Chutki Real": "Chutki from Chota Bheem, photorealistic real Indian girl with two ponytails, pink dress, cute, 8k",
"Motu Patlu Real": "Motu Patlu in real life, photorealistic two middle aged Indian men, one fat bald with moustache eating samosa, one thin, Furfuri Nagar, ultra detailed, 8k",
"Motu Samosa Real": "Motu eating samosa, photorealistic real samosa with chutney, ultra detailed food photography, 8k",
"Doraemon Real": "Doraemon in real life, photorealistic blue robot cat with real fur texture, standing with Nobita, 8k",
"Shin Chan Real": "Shin Chan in real life, photorealistic 5 year old Japanese boy with big head, funny face, 8k, real skin texture"
}

st.title("Indian AI")

with st.popover("Tools & Presets"):
    st.selectbox("Mode",["Both","Text","Image"],key="mode")
    st.markdown("**Cartoon → Real Image Presets**")
    sel = st.selectbox("Choose preset", [k for k in PRESETS.keys() if "---" not in k])
    if st.button("Use this prompt", use_container_width=True):
        st.session_state.preset_prompt = PRESETS[sel]
    st.markdown("**Upload Files**")
    uploaded = st.file_uploader("Upload", type=["png","jpg","jpeg","webp","txt","pdf"], label_visibility="collapsed")
    if uploaded:
        save_path = GENERATED_DIR / f"upload_{uuid.uuid4().hex}_{uploaded.name}"
        save_path.write_bytes(uploaded.getvalue())
        st.success(f"Uploaded: {uploaded.name}")
        if uploaded.type.startswith("image"):
            st.image(str(save_path), width=200)

for i,m in enumerate(st.session_state.messages):
    with st.container(border=True):
        if m["role"]=="user": st.markdown("**You**"); st.code(m["content"])
        elif m["type"]=="text": st.markdown("**Indian AI**"); st.code(m["content"]); copy_button(m["content"],i); st.download_button("Download",m["content"],file_name="response.txt",key=f"t{i}")
        elif m["type"]=="image" and os.path.exists(m["path"]): st.markdown("**Indian AI**"); st.image(m["path"],use_container_width=True); st.download_button("Download image",open(m["path"],"rb").read(),file_name=Path(m["path"]).name,key=f"im{i}")

with st.form("f",clear_on_submit=True):
    q=st.text_input("msg", value=st.session_state.preset_prompt, placeholder="Ask anything or use preset above...", label_visibility="collapsed")
    go=st.form_submit_button("Send",use_container_width=True)

if go and q.strip():
    q=q.strip()
    st.session_state.preset_prompt=""
    st.session_state.messages.append({"role":"user","type":"text","content":q})
    mode=st.session_state.mode
    if mode in ["Both","Text"]:
        try:
            with st.spinner("Generating..."): ans=generate_text(q)
            st.session_state.messages.append({"role":"assistant","type":"text","content":ans})
        except Exception as e: st.error(str(e))
    if mode in ["Both","Image"]:
        try:
            with st.spinner("Creating image..."): ip=generate_image(q)
            st.session_state.messages.append({"role":"assistant","type":"image","path":ip})
        except Exception as e: st.error(str(e))
    st.rerun()
