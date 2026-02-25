import streamlit as st
import random

# --- 1. SETTINGS & THEMING ---
st.set_page_config(page_title="Sorcery Sums: High School Edition", page_icon="🪄")

st.markdown(f"""
    <style>
    .stApp {{
        background-color: #fde4f2;
    }}
    .math-text {{
        color: #7b7dbd;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 3px dashed #c6c7ff;
    }}
    h1, h2, h3, p, span, label {{
        color: #7b7dbd !important;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }}
    .stButton>button {{
        background-color: #c6c7ff;
        color: white;
        border-radius: 20px;
        width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE HEADER ---
st.image("Sorcery Sums.png", use_container_width=True)

# --- 3. HIGH SCHOOL MATH GENERATOR ---
def generate_algebra_spell():
    # Creating an equation: ax + b = c
    x_target = random.randint(1, 12) # This is the answer the user needs to find
    a = random.randint(2, 10)
    b = random.randint(1, 20)
    c = (a * x_target) + b
    
    question = f"{a}x + {b} = {c}"
    return question, x_target

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'current_q' not in st.session_state:
    st.session_state.current_q, st.session_state.target_x = generate_algebra_spell()

# --- 4. THE INTERFACE ---
st.markdown("### 🔮 The Forbidden Algebra")
st.markdown(f'<div class="math-text">Solve for x: <br> {st.session_state.current_q}</div>', unsafe_allow_html=True)

user_answer = st.number_input("What is the value of x?", step=1, value=0)

if st.button("🪄 Cast Algebra Spell!"):
    if user_answer == st.session_state.target_x:
        st.balloons()
        st.success(f"Brilliant! x was indeed {st.session_state.target_x}. +20 Points")
        st.session_state.score += 20
        # Generate new question
        st.session_state.current_q, st.session_state.target_x = generate_algebra_spell()
        st.rerun()
    else:
        st.error("The equation remains sealed. Try again, Sorcerer!")

st.sidebar.markdown(f"## 🏆 Sorcerer Score: {st.session_state.score}")
