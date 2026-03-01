import streamlit as st
import random
import pandas as pd
import math
import time
import datetime
import numpy as np
import plotly.graph_objects as go 
import streamlit.components.v1 as components 
from streamlit_gsheets import GSheetsConnection

# --- 1. SETTINGS & THEMING ---
st.set_page_config(page_title="Sorcery Sums", page_icon="🪄", layout="centered")

# Track the Game Stage
if "app_stage" not in st.session_state:
    st.session_state.app_stage = "login"

# Autorefresh for Leaderboard
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=30000, key="datarefresh")
except:
    pass

# Dynamic Action Button (Enter vs Cast)
if st.session_state.app_stage == "login":
    button_image = "https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/enterrealm.png"
else:
    button_image = "https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/castspell.png"

st.markdown(f"""
    <style>
    /* 1. Main Background */
    .stApp {{ background-color: #f2e2ff; }}
    
    /* 2. Sidebar Background */
    [data-testid="stSidebar"] {{
        background-color: #ddfffc !important;
        border-right: 2px solid #c6c7ff;
    }}

    /* 3. RECTANGULAR SUBJECT BUTTONS (Stage 2) */
    div.stButton > button[kind="secondary"] {{
        background-color: transparent !important;
        border: none !important;
        color: transparent !important;
        background-size: contain !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        width: 100% !important;
        height: 85px !important;
        display: block !important;
        margin: 0 auto !important;
        transition: transform 0.2s ease;
        box-shadow: none !important;
    }}
    div.stButton > button[kind="secondary"]:hover {{ transform: scale(1.05); }}

    /* Mapping the 12 Rectangle Assets */
    button[key="alg10"] {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/algebra10.png") !important; }}
    button[key="alg11"] {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/algebra11.png") !important; }}
    button[key="alg12"] {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/algebra12.png") !important; }}
    
    button[key="quad10"] {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/quadratics10.png") !important; }}
    button[key="quad11"] {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/quadratics11.png") !important; }}
    button[key="quad12"] {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/quadratics12.png") !important; }}

    button[key="func10"] {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/functions10.png") !important; }}
    button[key="func11"] {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/functions11.png") !important; }}
    button[key="func12"] {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/functions12.png") !important; }}

    button[key="geo10"] {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/geometry10.png") !important; }}
    button[key="geo11"] {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/geometry11.png") !important; }}
    button[key="geo12"] {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/geometry12.png") !important; }}

    /* 4. MAIN ACTION BUTTON (Enter/Cast) */
    div.stButton > button:not([kind="secondary"]) {{
        background-image: url("{button_image}") !important;
        background-size: contain !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        width: 275px !important;
        height: 300px !important;
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
        display: block !important;
        margin: -80px auto 0 auto !important; 
    }}

    /* Global UI styles preserved from your code */
    .stExpander {{ background-color: rgba(255, 255, 255, 0.5); border-radius: 15px; }}
    .success-box {{ background-color: #ffffe3; border: 3px solid #b4a7d6; border-radius: 20px; padding: 20px; text-align: center; }}
    .success-box h2 {{ color: #7b7dbd !important; }}
    .question-container {{ background-color: white; padding: 30px; border-radius: 20px; border: 4px solid #c6c7ff; text-align: center; margin-top: 50px; }}
    div[data-testid="stTextInput"] input {{ background-color: #e6fff8 !important; text-align: center; }}
    div.stButton > button p {{ display: none !important; }}
    @keyframes floatUp {{ 0% {{ transform: translateY(0); opacity: 1; }} 100% {{ transform: translateY(-110vh); opacity: 0; }} }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE SACRED STAR EFFECT ---
def pastel_star_effect():
    components.html("""<script>
    const colors = ["#ffd6ff","#caffbf","#fdffb6","#bdb2ff","#a0c4ff"];
    for (let i = 0; i < 30; i++) {
        let star = window.parent.document.createElement("div");
        star.style.position = "fixed"; star.style.width = "25px"; star.style.height = "25px";
        star.style.clipPath = "polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)";
        star.style.left = Math.random() * 100 + "vw"; star.style.top = "100vh"; 
        star.style.background = colors[Math.floor(Math.random() * colors.length)];
        star.style.zIndex = "10000"; star.style.animation = "floatUp 2.5s ease-out forwards";
        window.parent.document.body.appendChild(star);
        setTimeout(() => star.remove(), 2500);
    }</script>""", height=0)

# --- 3. DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 4. MATH LOGIC (Preserved from original) ---
def generate_spell(unit, level):
    prog = int(level) - 9 
    def apply_sacred_style(fig):
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=20,r=20,t=20,b=20), height=400)
        return fig

    if "Algebra" in unit:
        a, x = random.randint(2, 5 * prog), random.randint(1, 12)
        b = random.randint(1, 10 * prog)
        c = (a * x) + b
        return f"Solve for x: {a}x + {b} = {c}", x, f"Scale: {a}x + {b} = {c}", None

    elif "Quadratics" in unit:
        h, k = random.randint(-3, 3), random.randint(1, 5)
        x_vals = np.linspace(h-5, h+5, 100)
        y_vals = (x_vals - h)**2 + k
        fig = go.Figure(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='black', width=3)))
        return "Find the vertex y-coordinate:", k, "Locate the lowest point.", apply_sacred_style(fig)

    elif "Functions" in unit:
        m, b_val = random.randint(1, 3), random.randint(-2, 2)
        tx = random.randint(-2, 2); ans = m * tx + b_val
        x_vals = np.linspace(-10, 10, 100)
        fig = go.Figure(go.Scatter(x=x_vals, y=m*x_vals+b_val, mode='lines', line=dict(color='black', width=3)))
        return f"Find f({tx})", ans, "Trace the path.", apply_sacred_style(fig)

    elif "Geometry" in unit:
        side = random.randint(3, 7 * prog)
        if level == "12": return f"Cube side is {side}. Find Volume.", side**3, f"3D Cube: {side}", None
        return f"Square side is {side}. Find Perimeter.", side * 4, f"Square: {side}", None
    return "Scroll lost", 0, "", None

# --- 5. STAGE 1: THE GATES (LOGIN) ---
if st.session_state.app_stage == "login":
    st.image("sorcerersums.png")
    name = st.text_input("", placeholder="Type your name here...", key="login_name", label_visibility="collapsed")
    if st.button("Enter Realm", key="enter_btn"):
        if name:
            st.session_state.player_name = name
            st.session_state.app_stage = "selection"
            st.rerun()

# --- 6. STAGE 2: THE SCROLL ROOM (SELECTION) ---
elif st.session_state.app_stage == "selection":
    st.image("choose_subject_title.png")
    
    # 4 rows of 3 columns
    subjects = [
        ("Algebra", "alg"), ("Quadratics", "quad"), 
        ("Functions", "func"), ("Geometry", "geo")
    ]
    
    for sub_name, sub_key in subjects:
        st.markdown(f"### {sub_name}")
        cols = st.columns(3)
        for i, grade in enumerate(["10", "11", "12"]):
            if cols[i].button(f"{sub_name} {grade}", key=f"{sub_key}{grade}", kind="secondary"):
                st.session_state.unit, st.session_state.level = sub_name, grade
                q, ans, img, plot = generate_spell(sub_name, grade)
                st.session_state.current_q, st.session_state.target_ans = q, ans
                st.session_state.current_image, st.session_state.current_plot = img, plot
                st.session_state.app_stage = "game"
                st.rerun()

# --- 7. STAGE 3: THE SPELL CHAMBER (GAME) ---
elif st.session_state.app_stage == "game":
    # Sidebar: Hall of Wizards
    st.sidebar.markdown("# 🏆 Hall of Wizards")
    try:
        df = conn.read(ttl=0)
        if not df.empty:
            st.sidebar.table(df.groupby("Name")["Score"].sum().sort_values(ascending=False).astype(int).head(10))
    except: pass
    
    if st.sidebar.button("📜 Change Scroll"):
        st.session_state.app_stage = "selection"
        st.rerun()

    st.image("Sorcery Sums.png")
    st.markdown(f"""<div class="question-container"><h3>Grade {st.session_state.level} {st.session_state.unit}</h3><h1>{st.session_state.current_q}</h1></div>""", unsafe_allow_html=True)

    with st.expander("🔮 Peer into the Crystal Ball"):
        st.write(st.session_state.current_image)
        if st.session_state.current_plot: st.plotly_chart(st.session_state.current_plot, use_container_width=True)

    st.text_area("Scratchpad:", placeholder="Work here...", height=100, key="pad")
    user_ans = st.text_input("Your Final Answer:", key="ans_input")

    if st.button("Cast Spell!", key="cast_btn"):
        try:
            if math.isclose(float(user_ans), st.session_state.target_ans, rel_tol=0.1):
                pastel_star_effect()
                st.markdown('<div class="success-box"><h2>Correct! (｡◕‿◕｡)━☆ﾟ.*･｡ﾟ</h2></div>', unsafe_allow_html=True)
                # Update GSheets
                new_row = pd.DataFrame([{"Name": st.session_state.player_name, "Score": 50, "Date": datetime.datetime.now().strftime("%Y-%m-%d")}])
                conn.update(data=pd.concat([conn.read(ttl=0), new_row], ignore_index=True))
                # New Question
                q, ans, img, plot = generate_spell(st.session_state.unit, st.session_state.level)
                st.session_state.current_q, st.session_state.target_ans = q, ans
                st.session_state.current_image, st.session_state.current_plot = img, plot
                time.sleep(1)
                st.rerun()
            else: st.error("The magic failed!")
        except: st.warning("Enter a number!")

