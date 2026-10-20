import os, uuid, base64
from pathlib import Path
from urllib.parse import quote
import requests
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
GENERATED_DIR = STATIC_DIR / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)
API_KEY = os.getenv("POLLINATIONS_API_KEY","").strip()

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
div[data-testid="stVerticalBlockBorderWrapper"],div[data-testid="stContainer"],div[data-testid="stForm"],div[data-testid="stPopoverBody"],div[data-testid="stChatMessage"]{{background:#000!important;border:1px solid #444!important;border-radius:12px!important}}
div[data-baseweb="select"],div[data-baseweb="select"]>div,div[role="listbox"],ul[role="listbox"]{{background:#000!important;color:#fff!important}}
li[role="option"]{{background:#000!important;color:#fff!important}}
div[data-testid="stCode"],div[data-testid="stCode"] pre{{background:#000!important;color:#fff!important;border:1px solid #444!important}}
.stButton button,.stDownloadButton button,div[data-testid="stFormSubmitButton"] button,[data-testid="stPopover"] button{{background:#000!important;color:#fff!important;border:1px solid #666!important}}
</style>""",unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages=[]
if "mode" not in st.session_state: st.session_state.mode="Both"
if "ghibli_prompt" not in st.session_state: st.session_state.ghibli_prompt=""

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

# GHIBLI PROMPTS
GHIBLI_PROMPTS = {
"Spirited Away Pork Buns": "Spirited Away steamed pork buns, photorealistic real food, fluffy baozi with juicy pork filling, steam rising, ultra detailed food photography, 8k, black background",
"Howl's Breakfast": "Howl's Moving Castle breakfast, real food, two fried eggs and bacon sizzling in cast iron pan, butter melting, photorealistic, 8k food photography",
"Ponyo Ramen": "Ponyo ramen, real ham ramen with boiled egg and green onions, steaming hot bowl, photorealistic, ultra detailed, Ghibli food to real life",
"Totoro Bento": "My Neighbor Totoro bento box, real Japanese lunch box with rice, shishamo fish, plum, photorealistic, studio lighting",
"Kiki's Chocolate Cake": "Kiki's Delivery Service chocolate cake, real bakery cake with chocolate frosting, photorealistic, 8k",
"Laputa Toast": "Castle in the Sky Laputa toast with fried egg on top, real thick toast, photorealistic breakfast, morning light, 8k",
"Spirited Away Onigiri": "Spirited Away onigiri rice balls, real Japanese onigiri with nori, salt crystals visible, photorealistic",
"Howl's Cheese Fondue": "Howl's Moving Castle cheese fondue, real melted cheese with bread dipping, photorealistic, cinematic lighting",
"Mononoke Soup": "Princess Mononoke mushroom soup, real forest mushroom soup in wooden bowl, photorealistic, steam",
"Totoro Strawberry Cake": "My Neighbor Totoro strawberry shortcake, real Japanese strawberry cake with cream and berries, photorealistic, 8k food photo"
}

st.title("Indian AI")

with st.popover("Tools"):
    st.selectbox("Mode",["Both","Text","Image"],key="mode")
    st.markdown("**Ghibli → Real Food Prompts**")
    sel = st.selectbox("Choose Ghibli Food", list(GHIBLI_PROMPTS.keys()))
    if st.button("Use this prompt"):
        st.session_state.ghibli_prompt = GHIBLI_PROMPTS[sel]

for i,m in enumerate(st.session_state.messages):
    with st.container(border=True):
        if m["role"]=="user": st.markdown("**You**"); st.code(m["content"])
        elif m["type"]=="text": st.markdown("**Indian AI**"); st.code(m["content"]); copy_button(m["content"],i); st.download_button("Download",m["content"],file_name="response.txt",key=f"t{i}")
        elif m["type"]=="image" and os.path.exists(m["path"]): st.markdown("**Indian AI**"); st.image(m["path"],use_container_width=True); st.download_button("Download image",open(m["path"],"rb").read(),file_name=Path(m["path"]).name,key=f"im{i}")

with st.form("f",clear_on_submit=True):
    q=st.text_input("msg", value=st.session_state.ghibli_prompt, placeholder="Ask anything or use Ghibli prompt...", label_visibility="collapsed")
    go=st.form_submit_button("Send",use_container_width=True)

if go and q.strip():
    q=q.strip()
    st.session_state.ghibli_prompt=""
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
