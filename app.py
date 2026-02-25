import streamlit as st
import random

# --- 1. SETTINGS & THEMING ---
st.set_page_config(page_title="Sorcery Sums", page_icon="🪄")

# Injecting your specific color scheme
# Background: #fde4f2 | Font/Accents: #c6c7ff
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #fde4f2;
    }}
    h1, h2, h3, p, span, label {{
        color: #7b7dbd !important; /* A darker version of c6c7ff for readability */
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }}
    .stButton>button {{
        background-color: #c6c7ff;
        color: white;
        border-radius: 20px;
        border: none;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE HEADER ---
# This assumes Sorcery Sums.png is in the same folder as app.py
st.image("Sorcery Sums.png", use_container_width=True)

# --- 3. GAME LOGIC ---
if 'score' not in st.session_state:
    st.session_state.score = 0

def generate_math_spell():
    num1 = random.randint(1, 12)
    num2 = random.randint(1, 12)
    return num1, num2, num1 + num2

if 'math_q' not in st.session_state:
    st.session_state.n1, st.session_state.n2, st.session_state.ans = generate_math_spell()

# --- 4. THE INTERFACE ---
st.markdown(f"### ✨ Magical Challenge: {st.session_state.n1} + {st.session_state.n2} = ?")

user_input = st.number_input("Cast your answer spell:", step=1, value=0)

if st.button("🪄 Cast Spell!"):
    if user_input == st.session_state.ans:
        st.balloons()
        st.success("Great Sorcery! +10 Points")
        st.session_state.score += 10
        # Refresh the question
        st.session_state.n1, st.session_state.n2, st.session_state.ans = generate_math_spell()
        st.rerun()
    else:
        st.error("The spell fizzled! Try again.")

st.sidebar.markdown(f"## 🏆 Score: {st.session_state.score}")
