import streamlit as st
import random
import pandas as pd
import math
from streamlit_gsheets import GSheetsConnection
from streamlit_autorefresh import st_autorefresh

# --- 1. SETTINGS & THEMING ---
st.set_page_config(page_title="Sorcery Sums", page_icon="🪄")

# Auto-refresh the app every 30 seconds to update the leaderboard
st_autorefresh(interval=30000, key="datarefresh")

st.markdown(f"""
    <style>
    .stApp {{
        background-color: #fde4f2;
    }}
    .math-card {{
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        border: 4px solid #c6c7ff;
        text-align: center;
        margin-bottom: 20px;
    }}
    h1, h2, h3, p, span, label, .stMarkdown {{
        color: #7b7dbd !important;
        font-family: 'Helvetica', sans-serif;
    }}
    .stButton>button {{
        background-color: #c6c7ff;
        color: white;
        border-radius: 50px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE CONNECTION ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("Connect your Google Sheet in Settings > Secrets to enable the Leaderboard!")

# --- 3. HIGH SCHOOL MATH ENGINE ---
def generate_advanced_spell():
    spell_type = random.choice(["Algebra", "Quadratic", "Geometry"])
    
    if spell_type == "Algebra":
        x = random.randint(2, 12)
        a, b = random.randint(2, 10), random.randint(1, 20)
        c = (a * x) + b
        return f"Solve for x: {a}x + {b} = {c}", x
    
    elif spell_type == "Quadratic":
        x = random.randint(2, 12)
        c = x**2
        return f"Solve for x: x² = {c}", x
    
    elif spell_type == "Geometry":
        r = random.randint(2, 10)
        # Find area of circle (rounded)
        area = round(math.pi * (r**2), 2)
        return f"A circle has an Area of {area}. What is its Radius (r)?", r

# --- 4. LOGIN & STATE ---
if "player_name" not in st.session_state:
    st.image("Sorcery Sums.png")
    st.title("🧙‍♂️ Sorcerer Login")
    name = st.text_input("Enter your name to join the duel:")
    if st.button("Enter Realm"):
        if name:
            st.session_state.player_name = name
            st.rerun()
    st.stop()

if 'current_q' not in st.session_state:
    st.session_state.current_q, st.session_state.target_ans = generate_advanced_spell()

# --- 5. MAIN INTERFACE ---
st.image("Sorcery Sums.png", use_container_width=True)
st.markdown(f"## Welcome, Archmage {st.session_state.player_name}")

st.markdown(f'<div class="math-card"><h1>{st.session_state.current_q}</h1></div>', unsafe_allow_html=True)

user_answer = st.number_input("Your Answer:", step=0.1)

if st.button("🪄 Cast Spell!"):
    if math.isclose(user_answer, st.session_state.target_ans, rel_tol=0.1):
        st.balloons()
        
        # SAVE TO GOOGLE SHEETS
        try:
            df = conn.read(worksheet="Sheet1")
            new_data = pd.DataFrame([{"Name": st.session_state.player_name, "Score": 50}])
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success("Great Sorcery! +50 Points saved to the scroll.")
        except:
            st.warning("Score not saved (Check your Google Sheet connection).")
            
        st.session_state.current_q, st.session_state.target_ans = generate_advanced_spell()
        st.rerun()
    else:
        st.error("The magic failed! Try a different calculation.")

# --- 6. LIVE LEADERBOARD ---
st.sidebar.markdown("# 🏆 Hall of Wizards")
try:
    scores_df = conn.read(worksheet="Sheet1")
    leaderboard = scores_df.groupby("Name")["Score"].sum().sort_values(ascending=False).head(10)
    st.sidebar.table(leaderboard)
except:
    st.sidebar.write("The scrolls are empty. Be the first to score!")
