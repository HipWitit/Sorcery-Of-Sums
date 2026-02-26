import streamlit as st
import random
import pandas as pd
import math
import time
import datetime
import numpy as np
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

    /* 3. PINK PODS FOR SELECTION (From the version you liked) */
    div[data-testid="stSelectbox"], 
    div[role="radiogroup"] {{
        background-color: #ffdef2 !important;
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #eecbff;
        margin-bottom: 15px;
    }}

    /* 4. PERIWINKLE CRYSTAL BALL FONT */
    .stExpander {{
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 15px;
    }}
    /* Forces the text inside the expander to be visible periwinkle */
    .stExpander p, .stExpander span, .stExpander label {{
        color: #7b7dbd !important;
        font-weight: bold;
    }}

    /* 5. YELLOW SUCCESS BOX FONT FIX (#f2e2ff) */
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

    /* 6. GLOBAL SIDEBAR TEXT & RADIOS */
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

    /* Input Field Styling */
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

# --- 5. MATH LOGIC WITH PROGRESSION & VISUALS ---
def generate_spell(unit, level):
    prog = int(level) - 9 
    plot_data = None
    
    if "Algebra" in unit:
        a = random.randint(2, 5 * prog)
        b = random.randint(1, 10 * prog)
        x = random.randint(1, 12)
        c = (a * x) + b
        image_tag = f"Imagine a balance scale. On one side, you have {a} mystery boxes (x) and {b} gems. On the other side, there are {c} gems."
        return f"Solve for x: {a}x + {b} = {c}", x, image_tag, None

    elif "Quadratics" in unit:
        h = random.randint(-2, 2)
        k = random.randint(1, 5)
        x_vals = np.linspace(h-5, h+5, 50)
        y_vals = (x_vals - h)**2 + k
        plot_data = pd.DataFrame({'x': x_vals, 'Energy (y)': y_vals}).set_index('x')
        image_tag = "A magic portal forms a curve. Scry the crystal ball to find the y-value of the vertex (the lowest point)."
        return f"Based on the graph, what is the y-coordinate of the vertex?", k, image_tag, plot_data

    elif "Functions" in unit:
        m = random.randint(1, 3)
        b = random.randint(-2, 2)
        target_x = random.randint(-2, 2)
        ans = m * target_x + b
        x_vals = np.linspace(-5, 5, 11)
        y_vals = m * x_vals + b
        plot_data = pd.DataFrame({'x': x_vals, 'Spell Power (y)': y_vals}).set_index('x')
        image_tag = f"A spell machine follows a linear path. Locate the point where x = {target_x}."
        return f"Using the graph, find the value of f({target_x})", ans, image_tag, plot_data

    elif "Geometry" in unit:
        side = random.randint(3, 7 * prog)
        if level == "12":
            ans = side**3
            image_tag = f"A 3D magic cube has sides of {side}. Calculate the total volume inside."
            return f"The side of a cube is {side}. What is its Volume?", ans, image_tag, None
        else:
            ans = side * 4
            image_tag = f"A square tile has a side of {side}. How long is the magic border around it?"
            return f"A square has a side of {side}. What is its Perimeter?", ans, image_tag, None
    
    return "Scroll not found", 0, "", None

# --- 6. SIDEBAR: LESSON SELECTION & LEADERBOARD ---
st.sidebar.title("📜 Choose Your Scroll")

unit_choice = st.sidebar.selectbox("Select Subject", ["Algebra", "Quadratics", "Functions", "Geometry"])
level_choice = st.sidebar.radio("Select Grade Level", ["10", "11", "12"])

if ("last_unit" not in st.session_state or 
    st.session_state.last_unit != unit_choice or 
    st.session_state.last_level != level_choice):
    st.session_state.last_unit = unit_choice
    st.session_state.last_level = level_choice
    q, ans, img, pdf = generate_spell(unit_choice, level_choice)
    st.session_state.current_q = q
    st.session_state.target_ans = ans
    st.session_state.current_image = img
    st.session_state.current_plot = pdf

st.sidebar.markdown("---")
st.sidebar.markdown("# 🏆 Hall of Wizards")
try:
    scores_df = conn.read(ttl=0)
    if not scores_df.empty:
        scores_df['Date'] = pd.to_datetime(scores_df['Date'])
        now = datetime.datetime.now()
        tab_w, tab_
