import streamlit as st
import random
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- 1. SETTINGS & THEMING ---
st.set_page_config(page_title="Sorcery Sums", page_icon="🪄")

# (Keep your existing CSS here for the pink background and fonts)

# --- 2. DATABASE CONNECTION ---
# Note: You'll need to add your Google Sheet URL in Streamlit Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 3. LOGIN & STATE ---
if "player_name" not in st.session_state:
    st.image("Sorcery Sums.png")
    st.title("Enter the Magic Realm")
    name = st.text_input("What is your Sorcerer Name?")
    if st.button("Begin Ritual"):
        st.session_state.player_name = name
        st.rerun()
    st.stop() # Prevents the rest of the app from running until named

# --- 4. GAME LOGIC ---
def generate_algebra_spell():
    x_target = random.randint(1, 12)
    a = random.randint(2, 10)
    b = random.randint(1, 20)
    c = (a * x_target) + b
    return f"{a}x + {b} = {c}", x_target

if 'current_q' not in st.session_state:
    st.session_state.current_q, st.session_state.target_x = generate_algebra_spell()

# --- 5. THE INTERFACE ---
st.image("Sorcery Sums.png", use_container_width=True)
st.markdown(f"### 🔮 Spell for {st.session_state.player_name}")
st.markdown(f'<div style="font-size:24px; color:#7b7dbd;">Solve: {st.session_state.current_q}</div>', unsafe_allow_html=True)

user_answer = st.number_input("Value of x:", step=1)

if st.button("🪄 Cast Spell!"):
    if user_answer == st.session_state.target_x:
        st.balloons()
        
        # SAVE TO GOOGLE SHEETS
        # Fetch current scores
        existing_data = conn.read(worksheet="Sheet1")
        new_row = pd.DataFrame([{"Name": st.session_state.player_name, "Score": 20}])
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        
        # Update the cloud
        conn.update(worksheet="Sheet1", data=updated_df)
        
        st.success("Score Recorded in the Clouds!")
        st.session_state.current_q, st.session_state.target_x = generate_algebra_spell()
        st.rerun()

# --- 6. LEADERBOARD ---
st.sidebar.title("🏆 Hall of Wizards")
try:
    scores_df = conn.read(worksheet="Sheet1")
    # Group by name and show top sorcerers
    leaderboard = scores_df.groupby("Name")["Score"].sum().sort_values(ascending=False)
    st.sidebar.table(leaderboard)
except:
    st.sidebar.write("Leaderboard is empty... for now.")
