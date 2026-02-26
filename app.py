import streamlit as st
import random
import pandas as pd
import math
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
from streamlit_gsheets import GSheetsConnection

# --- 1. SETTINGS & THEMING ---
st.set_page_config(page_title="Sorcery Sums", page_icon="🪄")

# Autorefresh for Leaderboard
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=30000, key="datarefresh")
except:
    pass

st.markdown(f"""
    <style>
    /* 1. Main Background */
    .stApp {{ background-color: #fde4f2; }}
    
    /* 2. Sidebar Background */
    [data-testid="stSidebar"] {{
        background-color: #ddfffc !important;
        border-right: 2px solid #c6c7ff;
    }}

    /* 3. PINK PODS FOR SELECTION (The Sacred Layout) */
    div[data-testid="stSelectbox"], 
    div[role="radiogroup"] {{
        background-color: #ffdef2 !important;
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #eecbff;
        margin-bottom: 15px;
    }}

    /* 4. WHITE GRAPH BACKGROUND FIX */
    div[data-testid="stChart"] {{
        background-color: white !important;
        padding: 10px;
        border-radius: 15px;
        border: 2px solid #7b7dbd;
    }}

    /* 5. PERIWINKLE CRYSTAL BALL FONT */
    .stExpander {{
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 15px;
    }}
    .stExpander p, .stExpander span, .stExpander label {{
        color: #7b7dbd !important;
        font-weight: bold;
    }}

    /* 6. YELLOW SUCCESS BOX FONT FIX */
    .success-box {{
        background-color: #ffffe3; 
        border: 3px solid #b4a7d6; 
        border-radius: 20px; 
        padding: 20px; 
        text-align: center; 
        margin-top: 15px; 
        margin-bottom: 15px;
    }}
    .success-box h2 {{
        color: #f2e2ff !important;
        text-shadow: 1px 1px 2px #7b7dbd;
        margin: 0; 
        font-size: 24px;
    }}

    /* 7. GLOBAL SIDEBAR TEXT & RADIOS */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] label p {{
        color: #7b7dbd !important;
    }}
    
    div[role="radiogroup"] div[data-testid="stRadioButtonInternalDefaultCircle"] {{
        border-color: #7b7dbd !important;
    }}
    div[role="radiogroup"] div[data-selection="true"] div {{
        background-color: #c6c7ff !important;
    }}
    
    .question-container {{
        background-color: white; 
        padding: 30px; 
        border-radius: 20px; 
        border: 4px solid #c6c7ff; 
        text-align: center; 
        margin-bottom: 20px;
    }}
    .question-container h1, .question-container h3 {{
        color: #7b7dbd !important;
    }}

    div[data-testid="stTextArea"] textarea {{
        background-color: #b4a7d6 !important; 
        color: #d4ffea !important;           
        border-radius: 10px;
    }}
    div[data-testid="stTextInput"] input {{
        background-color: #e6fff8 !important;
        color: #7b7dbd !important;
    }}
    .stButton>button {{ 
        background-color: #c6c7ff; 
        color: white; 
        border-radius: 50px; 
        width: 100%; 
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE SACRED STAR EFFECT ---
def pastel_star_effect():
    st.markdown("""
    <style>
    .star {
        position: fixed; width: 25px; height: 25px;
        clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
        animation: floatUp 2.5s ease-out forwards; z-index: 9999;
    }
    @keyframes floatUp {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-500px) rotate(360deg); opacity: 0; }
    }
    </style>
    <script>
    const colors = ["#ffd6ff","#caffbf","#fdffb6","#bdb2ff","#a0c4ff"];
    for (let i = 0; i < 30; i++) {
        let star = document.createElement("div");
        star.className = "star";
        star.style.left = Math.random() * window.innerWidth + "px";
        star.style.top = window.innerHeight + "px";
        star.style.background = colors[Math.floor(Math.random() * colors.length)];
        document.body.appendChild(star);
        setTimeout(() => star.remove(), 2500);
    }
    </script>
    """, unsafe_allow_html=True)

# --- 3. DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 4. LOGIN SCREEN ---
if "player_name" not in st.session_state:
    try:
        st.image("Sorcerer Login.png")
    except:
        st.write("✨ **Portal Opening...** ✨")
    name = st.text_input("Enter your name to begin your journey:")
    if st.button("Enter Realm"):
        if name:
            st.session_state.player_name = name
            st.rerun()
    st.stop()

# --- 5. MATH LOGIC WITH MATPLOTLIB GRAPHS ---
def generate_spell(unit, level):
    prog = int(level) - 9 
    fig = None
    
    if "Algebra" in unit:
        a = random.randint(2, 5 * prog)
        b = random.randint(1, 10 * prog)
        x = random.randint(1, 12)
        c = (a * x) + b
        image_tag = f"Imagine a balance scale. Side A: {a} mystery boxes (x) + {b} gems. Side B: {c} gems."
        return f"Solve for x: {a}x + {b} = {c}", x, image_tag, None

    elif "Quadratics" in unit:
        h = random.randint(-3, 3) 
        k = random.randint(1, 5)  
        x_vals = np.linspace(h-5, h+5, 100)
        y_vals = (x_vals - h)**2 + k
        
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(x_vals, y_vals, color='black', linewidth=2)
        ax.set_facecolor('white')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
        ax.axhline(y=0, color='black', linewidth=1.5)
        ax.axvline(x=0, color='black', linewidth=1.5)
        
        image_tag = "A magic portal forms a curve. Scry the crystal ball for the lowest point (the vertex)."
        return f"What is the y-coordinate of the vertex in the graph?", k, image_tag, fig

    elif "Functions" in unit:
        m = random.randint(1, 3); b_val = random.randint(-2, 2)
        target_x = random.randint(-2, 2); ans = m * target_x + b_val
        x_vals = np.linspace(-10, 10, 100)
        y_vals = m * x_vals + b_val
        
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(x_vals, y_vals, color='black', linewidth=2)
        ax.set_facecolor('white')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
        ax.axhline(y=0, color='black', linewidth=1.5)
        ax.axvline(x=0, color='black', linewidth=1.5)
        ax.set_xlim([-10, 10])
        ax.set_ylim([-10, 10])

        image_tag = f"The spell line follows a constant path. Locate where x = {target_x}."
        return f"Using the graph aid, find f({target_x})", ans, image_tag, fig

    elif "Geometry" in unit:
        side = random.randint(3, 7 * prog)
        if level == "12":
            ans = side**3
            return f"The side of a cube is {side}. Find Volume.", ans, f"A 3D cube with side {side}.", None
        ans = side * 4
        return f"A square has a side of {side}. Find Perimeter.", ans, f"A square with side {side}.", None
    
    return "Scroll not found", 0, "", None

# --- 6. SIDEBAR: SELECTION & LEADERBOARD ---
st.sidebar.title("📜 Choose Your Scroll")

unit_choice = st.sidebar.selectbox("Select Subject", ["Algebra", "Quadratics", "Functions", "Geometry"])
level_choice = st.sidebar.radio("Select Grade Level", ["10", "11", "12"])

if ("last_unit" not in st.session_state or 
    st.session_state.last_unit != unit_choice or 
    st.session_state.last_level != level_choice):
    st.session_state.last_unit = unit_choice
    st.session_state.last_level = level_choice
    q, ans, img, pdf = generate_spell(unit_choice, level_choice)
    st.session_state.current_q, st.session_state.target_ans = q, ans
    st.session_state.current_image, st.session_state.current_plot = img, pdf

st.sidebar.markdown("---")
st.sidebar.markdown("# 🏆 Hall of Wizards")
try:
    scores_df = conn.read(ttl=0)
    if not scores_df.empty:
        scores_df['Date'] = pd.to_datetime(scores_df['Date'])
        now = datetime.datetime.now()
        t1, t2, t3 = st.sidebar.tabs(["Week", "Month", "Year"])
        with t1:
            w_data = scores_df[scores_df['Date'] >= (now - datetime.timedelta(days=7))]
            if not w_data.empty: st.table(w_data.groupby("Name")["Score"].sum().sort_values(ascending=False).astype(int))
except:
    st.sidebar.write("The scrolls are sleeping.")

# --- 7. MAIN INTERFACE ---
try:
    st.image("Sorcery Sums.png")
except:
    st.title("Sorcery Sums")

st.markdown(f"""
    <div class="question-container">
        <h3>Grade {level_choice} {unit_choice}</h3>
        <h1>{st.session_state.current_q}</h1>
    </div>
""", unsafe_allow_html=True)

with st.expander("🔮 Peer into the Crystal Ball (Visual Aid)"):
    st.write(st.session_state.get('current_image', 'No visual found.'))
    if st.session_state.get('current_plot') is not None:
        # RENDERING THE MATPLOTLIB FIGURE
        st.pyplot(st.session_state.current_plot)

st.text_area("Spellbook Scratchpad:", placeholder="Work out equations...", height=100, key="scratchpad")
user_ans_raw = st.text_input("Your Final Answer:", placeholder="Type number here...")

if st.button("🪄 Cast Spell!"):
    try:
        if math.isclose(float(user_ans_raw), st.session_state.target_ans, rel_tol=0.1):
            pastel_star_effect()
            st.markdown('<div class="success-box"><h2>Correct! (｡◕‿◕｡)━☆ﾟ.*･｡ﾟ</h2></div>', unsafe_allow_html=True)
            time.sleep(1.0)
            try:
                df = conn.read(ttl=0)
                new_row = pd.DataFrame([{"Name": st.session_state.player_name, "Score": 50, "Date": datetime.datetime.now().strftime("%Y-%m-%d")}])
                conn.update(data=pd.concat([df, new_row], ignore_index=True))
            except: pass
            
            q, ans, img, pdf = generate_spell(unit_choice, level_choice)
            st.session_state.current_q, st.session_state.target_ans = q, ans
            st.session_state.current_image, st.session_state.current_plot = img, pdf
            st.rerun()
        else: st.error("The magic failed!")
    except: st.warning("Enter a number!")
