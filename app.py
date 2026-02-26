import streamlit as st
import random
import pandas as pd
import math
import time
import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. SETTINGS & THEMING ---
st.set_page_config(page_title="Sorcery Sums", page_icon="🪄")

# Autorefresh safety
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=30000, key="datarefresh")
except:
    pass

st.markdown(f"""
    <style>
    .stApp {{ background-color: #fde4f2; }}
    h1, h2, h3, p, span, label {{ color: #7b7dbd !important; font-family: 'Helvetica', sans-serif; }}
    
    .question-container {{
        background-color: white; 
        padding: 30px; 
        border-radius: 20px; 
        border: 4px solid #c6c7ff; 
        text-align: center; 
        margin-bottom: 20px;
    }}

    div[data-testid="stTextArea"] textarea {{
        background-color: #b4a7d6 !important; 
        color: #d4ffea !important;           
        border-radius: 10px;
        border: 2px solid #7b7dbd;
        font-family: 'Helvetica', sans-serif;
    }}
    
    div[data-testid="stTextInput"] input {{
        background-color: #e6fff8 !important;
        color: #7b7dbd !important;
        border-radius: 10px;
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
        position: fixed;
        width: 25px;
        height: 25px;
        clip-path: polygon(
            50% 0%, 61% 35%, 98% 35%,
            68% 57%, 79% 91%,
            50% 70%, 21% 91%,
            32% 57%, 2% 35%,
            39% 35%
        );
        animation: floatUp 2.5s ease-out forwards;
        z-index: 9999;
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

# --- 3. DATABASE & LOGIN ---
conn = st.connection("gsheets", type=GSheetsConnection)

if "player_name" not in st.session_state:
    try:
        st.image("Sorcerer Login.png")
    except:
        st.write("✨ **Portal Opening...** ✨")
    name = st.text_input("Enter your name:")
    if st.button("Enter Realm"):
        if name:
            st.session_state.player_name = name
            st.rerun()
    st.stop()

# --- 4. MATH LOGIC ---
def generate_advanced_spell():
    spell_type = random.choice(["Algebra", "Quadratic", "Geometry"])
    if spell_type == "Algebra":
        x = random.randint(2, 12)
        a, b = random.randint(2, 10), random.randint(1, 20)
        c = (a * x) + b
        return f"Solve for x: {a}x + {b} = {c}", x
    elif spell_type == "Quadratic":
        x = random.randint(2, 12)
        return f"Solve for x: x² = {x**2}", x
    elif spell_type == "Geometry":
        r = random.randint(2, 10)
        area = round(math.pi * (r**2), 2)
        return f"Circle Area = {area}. What is r?", r

if 'current_q' not in st.session_state:
    st.session_state.current_q, st.session_state.target_ans = generate_advanced_spell()

# --- 5. MAIN INTERFACE ---
try:
    st.image("Sorcery Sums.png")
except:
    st.title("Sorcery Sums")

st.markdown(f'<div class="question-container"><h1>{st.session_state.current_q}</h1></div>', unsafe_allow_html=True)

st.text_area("Spellbook Scratchpad:", placeholder="Work out your equations...", height=100, key="scratchpad")

user_answer_raw = st.text_input("Your Final Answer:", placeholder="Type number here...")

if st.button("🪄 Cast Spell!"):
    try:
        user_answer = float(user_answer_raw)
        if math.isclose(user_answer, st.session_state.target_ans, rel_tol=0.1):
            # TRIGGER YOUR CUSTOM EFFECT
            pastel_star_effect()
            st.toast("Correct! (｡◕‿◕｡)━☆ﾟ.*･｡ﾟ", icon="✨")
            
            try:
                df = conn.read(ttl=0)
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                new_row = pd.DataFrame([{"Name": st.session_state.player_name, "Score": 50, "Date": current_date}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.success("✨ Score recorded! ✨")
                time.sleep(1.5) 
            except Exception as e:
                st.error(f"⚠️ DATABASE ERROR: {e}")
            
            st.session_state.current_q, st.session_state.target_ans = generate_advanced_spell()
            st.rerun()
        else:
            st.error("The magic failed! (╥﹏╥)")
    except ValueError:
        st.warning("🔮 Please enter a numeric answer!")

# --- 6. LEADERBOARD ---
st.sidebar.markdown("# 🏆 Hall of Wizards")
try:
    scores_df = conn.read(ttl=0)
    if not scores_df.empty:
        scores_df['Date'] = pd.to_datetime(scores_df['Date'])
        now = datetime.datetime.now()
        tab_week, tab_month, tab_year = st.sidebar.tabs(["Week", "Month", "Year"])
        
        with tab_week:
            week_data = scores_df[scores_df['Date'] >= (now - datetime.timedelta(days=7))]
            if not week_data.empty:
                st.table(week_data.groupby("Name")["Score"].sum().sort_values(ascending=False).astype(int))
        # [Remaining sidebar tabs unchanged]
except:
    st.sidebar.write("The scrolls are sleeping.")
