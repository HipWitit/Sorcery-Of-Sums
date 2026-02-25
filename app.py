import streamlit as st
import random
import pandas as pd
import math
import time
import datetime  # NEW: Needed for time-traveling logic
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
    div[data-baseweb="input"] {{ background-color: #e6fff8 !important; border-radius: 10px; }}
    input {{ color: #9eb6ff !important; background-color: #e6fff8 !important; }}
    .stButton>button {{ background-color: #c6c7ff; color: white; border-radius: 50px; width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 3. LOGIN SCREEN ---
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

st.markdown(f'<div style="background-color: white; padding: 30px; border-radius: 20px; border: 4px solid #c6c7ff; text-align: center; margin-bottom: 20px;"><h1>{st.session_state.current_q}</h1></div>', unsafe_allow_html=True)

user_answer = st.number_input("Your Answer:", step=0.1)

if st.button("🪄 Cast Spell!"):
    if math.isclose(user_answer, st.session_state.target_ans, rel_tol=0.1):
        st.balloons()
        try:
            df = conn.read(ttl=0)
            
            # STAMP THE DATE (YYYY-MM-DD)
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # ADD DATA WITH DATE COLUMN
            new_row = pd.DataFrame([{
                "Name": st.session_state.player_name, 
                "Score": 50, 
                "Date": current_date
            }])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
            conn.update(data=updated_df)
            st.success("✨ Score recorded! ✨")
            time.sleep(1)
            
        except Exception as e:
            st.error(f"⚠️ DATABASE ERROR: {e}")
            time.sleep(5)
        
        st.session_state.current_q, st.session_state.target_ans = generate_advanced_spell()
        st.rerun()
    else:
        st.error("The magic failed!")

# --- 6. LEADERBOARD (WEEK, MONTH, YEAR) ---
st.sidebar.markdown("# 🏆 Hall of Wizards")
try:
    scores_df = conn.read(ttl=0)
    if not scores_df.empty:
        # Convert 'Date' column to actual datetime objects for filtering
        scores_df['Date'] = pd.to_datetime(scores_df['Date'])
        now = datetime.datetime.now()

        # Create the Tabs
        tab_week, tab_month, tab_year = st.sidebar.tabs(["Week", "Month", "Year"])

        with tab_week:
            # Last 7 days
            week_filter = now - datetime.timedelta(days=7)
            week_data = scores_df[scores_df['Date'] >= week_filter]
            if not week_data.empty:
                st.table(week_data.groupby("Name")["Score"].sum().sort_values(ascending=False).astype(int))
            else:
                st.write("No spells cast this week.")

        with tab_month:
            # Current calendar month
            month_data = scores_df[scores_df['Date'].dt.month == now.month]
            if not month_data.empty:
                st.table(month_data.groupby("Name")["Score"].sum().sort_values(ascending=False).astype(int))
            else:
                st.write("No spells cast this month.")

        with tab_year:
            # Current calendar year
            year_data = scores_df[scores_df['Date'].dt.year == now.year]
            if not year_data.empty:
                st.table(year_data.groupby("Name")["Score"].sum().sort_values(ascending=False).astype(int))
            else:
                st.write("No spells cast this year.")
    else:
        st.sidebar.write("The scrolls are empty.")
except Exception as e:
    st.sidebar.write(f"Can't reach the scrolls: {e}")
