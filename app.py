import streamlit as st
import random
import pandas as pd
import math
from streamlit_gsheets import GSheetsConnection

# --- 1. SETTINGS & THEMING ---
st.set_page_config(page_title="Sorcery Sums", page_icon="🪄")

# Safety check for the autorefresh library
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=30000, key="datarefresh")
except ImportError:
    pass

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
        font-weight: bold;
        width: 100%;
    }}
    /* Removes the padding at the top of the page for a cleaner look */
    .block-container {{
        padding-top: 2rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE CONNECTION ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    pass

# --- 3. LOGIN SCREEN ---
if "player_name" not in st.session_state:
    try:
        # This replaces the text/emoji header
        st.image("Sorcerer Login.png", width="stretch")
    except:
        st.write("✨ **The Portal is Opening...** ✨")
        
    name = st.text_input("Enter your name to join the duel:")
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
        return f"A circle has an Area of {area}. What is its Radius (r)?", r

if 'current_q' not in st.session_state:
    st.session_state.current_q, st.session_state.target_ans = generate_advanced_spell()

# --- 5. MAIN INTERFACE ---
try:
    st.image("Sorcery Sums.png", width="stretch")
except:
    st.title("Sorcery Sums")

st.markdown(f"## Welcome, Archmage {st.session_state.player_name}")

st.markdown(f'<div class="math-card"><h1>{st.session_state.current_q}</h1></div>', unsafe_allow_html=True)

user_answer = st.number_input("Your Answer:", step=0.1)

if st.button("🪄 Cast Spell!"):
    if math.isclose(user_answer, st.session_state.target_ans, rel_tol=0.1):
        st.balloons()
        try:
            df = conn.read(worksheet="Sheet1")
            new_data = pd.DataFrame([{"Name": st.session_state.player_name, "Score": 50}])
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
        except:
            pass
        st.session_state.current_q, st.session_state.target_ans = generate_advanced_spell()
        st.rerun()
    else:
        st.error("The magic failed!")

# --- 6. LEADERBOARD ---
st.sidebar.markdown("# 🏆 Hall of Wizards")
try:
    scores_df = conn.read(worksheet="Sheet1")
    leaderboard = scores_df.groupby("Name")["Score"].sum().sort_values(ascending=False).head(10)
    st.sidebar.table(leaderboard)
except:
    st.sidebar.write("The scrolls are empty.")
