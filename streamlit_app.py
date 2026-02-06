import streamlit as st
import threading, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import database as db

st.set_page_config(page_title="Waleed Automation", page_icon="🔥", layout="wide")

# ------------------------------------------------------------------------------------
# 🔥 KEEP ALIVE SYSTEM - Server ko band nahi hone dega
# ------------------------------------------------------------------------------------
def keep_alive():
    """Streamlit server ko active rakhne ke liye"""
    if "last_ping" not in st.session_state:
        st.session_state.last_ping = time.time()
    
    # Har 30 second mein ping
    if time.time() - st.session_state.last_ping > 30:
        st.session_state.last_ping = time.time()

keep_alive()

# ------------------------------------------------------------------------------------
# 🔥 LIVE LOGS SYSTEM
# ------------------------------------------------------------------------------------
def init_live_logs(max_lines: int = 200):
    if "live_logs" not in st.session_state:
        st.session_state.live_logs = []
    if "live_logs_max" not in st.session_state:
        st.session_state.live_logs_max = max_lines

def live_log(msg: str):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"

    init_live_logs()
    st.session_state.live_logs.append(line)

    if len(st.session_state.live_logs) > st.session_state.live_logs_max:
        st.session_state.live_logs = st.session_state.live_logs[-st.session_state.live_logs_max:]

def render_live_console():
    st.markdown('<div class="logbox">', unsafe_allow_html=True)
    for line in st.session_state.live_logs[-100:]:
        st.markdown(line)
    st.markdown('</div>', unsafe_allow_html=True)
# ------------------------------------------------------------------------------------


# ---------------- 🎨 UNIQUE WALEED THEME CSS ----------------
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;700&display=swap');

/* Main Background with Animated Gradient */
.stApp {
    background: linear-gradient(-45deg, #0f0f23, #1a1a3e, #0d0d2b, #151530);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    font-family: 'Rajdhani', sans-serif;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Animated Particles Effect */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image: 
        radial-gradient(2px 2px at 20px 30px, #00ffff, transparent),
        radial-gradient(2px 2px at 40px 70px, #ff00ff, transparent),
        radial-gradient(2px 2px at 50px 160px, #00ff00, transparent),
        radial-gradient(2px 2px at 90px 40px, #ffff00, transparent),
        radial-gradient(2px 2px at 130px 80px, #00ffff, transparent),
        radial-gradient(2px 2px at 160px 120px, #ff00ff, transparent);
    background-repeat: repeat;
    background-size: 200px 200px;
    animation: twinkle 5s ease-in-out infinite;
    opacity: 0.5;
    z-index: 0;
    pointer-events: none;
}

@keyframes twinkle {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 0.8; }
}

/* Glowing Header */
h1 {
    font-family: 'Orbitron', sans-serif !important;
    background: linear-gradient(90deg, #00ffff, #ff00ff, #00ff00, #00ffff);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientText 3s ease infinite;
    text-shadow: 0 0 30px rgba(0,255,255,0.5);
    font-size: 3rem !important;
    letter-spacing: 3px;
}

@keyframes gradientText {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Subheader Styling */
h2, h3, .stSubheader {
    font-family: 'Orbitron', sans-serif !important;
    color: #00ffff !important;
    text-shadow: 0 0 10px rgba(0,255,255,0.5);
}

/* Neon Log Box */
.logbox {
    background: linear-gradient(145deg, rgba(0,0,0,0.8), rgba(20,20,50,0.9));
    color: #00ff00;
    padding: 20px;
    height: 350px;
    overflow-y: auto;
    border-radius: 15px;
    border: 2px solid #00ffff;
    box-shadow: 
        0 0 20px rgba(0,255,255,0.4),
        0 0 40px rgba(0,255,255,0.2),
        inset 0 0 20px rgba(0,255,255,0.1);
    font-family: 'Courier New', monospace;
    font-size: 14px;
    line-height: 1.6;
}

.logbox::-webkit-scrollbar {
    width: 8px;
}

.logbox::-webkit-scrollbar-track {
    background: rgba(0,0,0,0.3);
    border-radius: 10px;
}

.logbox::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00ffff, #ff00ff);
    border-radius: 10px;
}

/* Neon Buttons */
.stButton > button {
    background: linear-gradient(145deg, #1a1a3e, #0d0d2b) !important;
    color: #00ffff !important;
    border: 2px solid #00ffff !important;
    border-radius: 10px !important;
    padding: 15px 30px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: bold !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 15px rgba(0,255,255,0.3) !important;
}

.stButton > button:hover {
    background: linear-gradient(145deg, #00ffff, #00cccc) !important;
    color: #000 !important;
    box-shadow: 0 0 30px rgba(0,255,255,0.8) !important;
    transform: translateY(-2px) !important;
}

.stButton > button:disabled {
    background: linear-gradient(145deg, #333, #222) !important;
    color: #666 !important;
    border-color: #444 !important;
    box-shadow: none !important;
}

/* Input Fields */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(0,0,0,0.6) !important;
    color: #00ffff !important;
    border: 2px solid #333 !important;
    border-radius: 10px !important;
    font-family: 'Rajdhani', sans-serif !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #00ffff !important;
    box-shadow: 0 0 15px rgba(0,255,255,0.4) !important;
}

/* Select Box */
.stSelectbox > div > div {
    background: rgba(0,0,0,0.6) !important;
    border: 2px solid #333 !important;
    border-radius: 10px !important;
}

/* Number Input */
.stNumberInput > div > div > input {
    background: rgba(0,0,0,0.6) !important;
    color: #00ffff !important;
    border: 2px solid #333 !important;
    border-radius: 10px !important;
}

/* File Uploader */
.stFileUploader > div {
    background: rgba(0,0,0,0.4) !important;
    border: 2px dashed #00ffff !important;
    border-radius: 15px !important;
    padding: 20px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: rgba(0,0,0,0.3);
    padding: 10px;
    border-radius: 15px;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(0,0,0,0.5) !important;
    color: #00ffff !important;
    border-radius: 10px !important;
    border: 1px solid #333 !important;
    font-family: 'Orbitron', sans-serif !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(145deg, #00ffff, #00cccc) !important;
    color: #000 !important;
}

/* Success/Error Messages */
.stSuccess {
    background: linear-gradient(145deg, rgba(0,100,0,0.3), rgba(0,50,0,0.5)) !important;
    border: 1px solid #00ff00 !important;
    border-radius: 10px !important;
    color: #00ff00 !important;
}

.stError {
    background: linear-gradient(145deg, rgba(100,0,0,0.3), rgba(50,0,0,0.5)) !important;
    border: 1px solid #ff0000 !important;
    border-radius: 10px !important;
    color: #ff0000 !important;
}

/* Sidebar */
.css-1d391kg, [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a1a, #1a1a3e) !important;
    border-right: 2px solid #00ffff !important;
}

/* Status Indicator */
.status-online {
    display: inline-block;
    width: 12px;
    height: 12px;
    background: #00ff00;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse 1.5s ease-in-out infinite;
    box-shadow: 0 0 10px #00ff00;
}

.status-offline {
    display: inline-block;
    width: 12px;
    height: 12px;
    background: #ff0000;
    border-radius: 50%;
    margin-right: 8px;
    box-shadow: 0 0 10px #ff0000;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.2); }
}

/* Glowing Card Effect */
.glow-card {
    background: linear-gradient(145deg, rgba(0,0,0,0.6), rgba(20,20,50,0.8));
    border: 1px solid rgba(0,255,255,0.3);
    border-radius: 20px;
    padding: 25px;
    margin: 15px 0;
    box-shadow: 
        0 0 20px rgba(0,255,255,0.1),
        inset 0 0 20px rgba(0,255,255,0.05);
}

/* Metric Display */
.metric-box {
    background: linear-gradient(145deg, rgba(0,255,255,0.1), rgba(255,0,255,0.1));
    border: 2px solid #00ffff;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 0 25px rgba(0,255,255,0.3);
}

.metric-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.5rem;
    color: #00ffff;
    text-shadow: 0 0 20px rgba(0,255,255,0.8);
}

.metric-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #0a0a1a;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00ffff, #ff00ff);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #00cccc, #cc00cc);
}
</style>

<!-- Keep Alive Script -->
<script>
    // Server ko active rakhne ke liye
    setInterval(function() {
        fetch(window.location.href, {method: 'HEAD'});
    }, 30000);
    
    // Page reload prevent
    window.onbeforeunload = null;
</script>
""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align:center;">⚡ WALEED E2EE SERVER ⚡</h1>', unsafe_allow_html=True)


# ---------------- SESSION ----------------
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "automation_running" not in st.session_state: st.session_state.automation_running = False
if "automation_state" not in st.session_state:
    st.session_state.automation_state = type('obj',(object,),{
        "running": False,
        "message_count": 0,
        "message_rotation_index": 0
    })()

init_live_logs()


# ---------------- LOGIN ----------------
if not st.session_state.logged_in:
    st.markdown('<div class="glow-card">', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 Login", "✨ Create Account"])
    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            uid = db.verify_user(u, p)
            if uid:
                st.session_state.logged_in = True
                st.session_state.user_id = uid
                cfg = db.get_user_config(uid)

                st.session_state.chat_id = cfg.get("chat_id", "")
                st.session_state.chat_type = cfg.get("chat_type", "E2EE")
                st.session_state.delay = cfg.get("delay", 15)
                st.session_state.cookies = cfg.get("cookies", "")
                st.session_state.messages = cfg.get("messages", "").split("\n") if cfg.get("messages") else []

                if cfg.get("running", False):
                    st.session_state.automation_running = True
                    st.session_state.automation_state.running = True

                st.rerun()
            else:
                st.error("Invalid login")

    with tab2:
        nu = st.text_input("New Username")
        np = st.text_input("New Password", type="password")
        npc = st.text_input("Confirm Password", type="password")
        if st.button("Create User"):
            if np != npc:
                st.error("Passwords do not match")
            else:
                ok, msg = db.create_user(nu, np)
                if ok: st.success("User created!")
                else: st.error(msg)
    st.markdown('</div>', unsafe_allow_html=True)

    st.stop()


# ---------------- DASHBOARD ----------------
# Status Indicator
if st.session_state.automation_running:
    st.markdown('<p><span class="status-online"></span> <strong style="color:#00ff00;">AUTOMATION RUNNING</strong></p>', unsafe_allow_html=True)
else:
    st.markdown('<p><span class="status-offline"></span> <strong style="color:#ff0000;">AUTOMATION STOPPED</strong></p>', unsafe_allow_html=True)

st.subheader(f"🎮 Dashboard — User: {st.session_state.user_id}")

if st.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.automation_running = False
    st.session_state.automation_state.running = False
    st.rerun()


# ---------------- MESSAGE FILE ----------------
st.markdown('<div class="glow-card">', unsafe_allow_html=True)
msg_file = st.file_uploader("📁 Upload .txt messages", type=["txt"])
if msg_file:
    st.session_state.messages = msg_file.read().decode().split("\n")
    st.success("✅ Messages Loaded")
st.markdown('</div>', unsafe_allow_html=True)


# ---------------- CONFIG ----------------
st.markdown('<div class="glow-card">', unsafe_allow_html=True)
st.subheader("⚙️ Configuration")
chat_id = st.text_input("💬 Chat ID", value=st.session_state.chat_id)
chat_type = st.selectbox("📱 Chat Type", ["E2EE", "CONVO"], index=0 if st.session_state.chat_type == "E2EE" else 1)
delay = st.number_input("⏱️ Delay (seconds)", 1, 300, value=st.session_state.delay)
cookies = st.text_area("🍪 Cookies", value=st.session_state.cookies)

if st.button("💾 Save Config"):
    db.update_user_config(
        st.session_state.user_id,
        chat_id, chat_type, delay,
        cookies, "\n".join(st.session_state.messages),
        running=st.session_state.automation_running
    )
    st.success("✅ Configuration Saved!")
st.markdown('</div>', unsafe_allow_html=True)


# ---------------- AUTOMATION ENGINE ----------------
def setup_browser():
    opt = Options()
    opt.add_argument("--headless=new")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=opt)

def find_input(driver, chat_type):
    sel = ["div[contenteditable='true']"] if chat_type == "E2EE" else ["div[contenteditable='true']", "textarea", "[role='textbox']"]
    for s in sel:
        try:
            return driver.find_element(By.CSS_SELECTOR, s)
        except: pass
    return None


def send_messages(cfg, stt):
    try:
        live_log("🚀 Starting browser...")
        d = setup_browser()
        d.get("https://www.facebook.com")
        time.sleep(8)
        live_log("✅ Facebook loaded")

        for c in (cfg.get("cookies") or "").split(";"):
            if "=" in c:
                n, v = c.split("=", 1)
                try:
                    d.add_cookie({"name":n.strip(), "value":v.strip(), "domain":".facebook.com", "path":"/"})
                except:
                    live_log(f"⚠️ Cookie failed: {c}")

        d.get(f"https://www.facebook.com/messages/t/{cfg.get('chat_id','')}")
        time.sleep(10)
        live_log("💬 Chat opened")

        box = find_input(d, cfg.get("chat_type"))
        if not box:
            live_log("❌ Input box not found")
            stt.running = False
            return

        msgs = [m.strip() for m in (cfg.get("messages") or "").split("\n") if m.strip()]
        if not msgs: msgs = ["Hello!"]

        while stt.running:
            msg = msgs[stt.message_rotation_index % len(msgs)]
            stt.message_rotation_index += 1

            try:
                box.send_keys(msg)
                box.send_keys("\n")
                stt.message_count += 1
                live_log(f"📤 Sent: {msg}")
            except Exception as e:
                live_log(f"❌ Error: {e}")

            time.sleep(cfg.get("delay", 15))

        live_log("🛑 Automation stopped")
        d.quit()

    except Exception as e:
        live_log(f"💥 Fatal Error: {e}")


# ---------------- CONTROLS ----------------
st.markdown('<div class="glow-card">', unsafe_allow_html=True)
st.subheader("🎛️ Automation Control")

col1, col2 = st.columns(2)

if col1.button("▶️ START", disabled=st.session_state.automation_running):
    cfg = db.get_user_config(st.session_state.user_id)
    cfg["running"] = True
    st.session_state.automation_running = True
    st.session_state.automation_state.running = True

    t = threading.Thread(target=send_messages, args=(cfg, st.session_state.automation_state))
    t.daemon = True
    t.start()

if col2.button("⏹️ STOP", disabled=not st.session_state.automation_running):
    st.session_state.automation_state.running = False
    st.session_state.automation_running = False
    live_log("🛑 Stop pressed. Automation halting...")
st.markdown('</div>', unsafe_allow_html=True)


# ---------------- STATS DISPLAY ----------------
st.markdown(f'''
<div class="metric-box">
    <div class="metric-value">{st.session_state.automation_state.message_count}</div>
    <div class="metric-label">Messages Sent</div>
</div>
''', unsafe_allow_html=True)


# ---------------- LIVE LOGS DISPLAY ----------------
st.subheader("📡 Live Console")

render_live_console()

# Keep refreshing when automation is running
if st.session_state.automation_running:
    time.sleep(1)
    st.rerun()
