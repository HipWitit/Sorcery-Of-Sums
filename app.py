import streamlit as st
import random
import sympy as sp 

# --- 1. SETTINGS & THEMING ---
st.set_page_config(page_title="Alchemical Altar", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #f2e2ff; }
    h1, h3, label p { color: #7b7dbd !important; text-align: center; }
    .equation-container {
        background-color: white; padding: 40px; border-radius: 20px; 
        border: 5px solid #c6c7ff; text-align: center; margin-top: 30px; margin-bottom: 30px;
    }
    .equation-text { font-size: 40px; color: #7b7dbd !important; font-weight: bold; }
    div[data-testid="stForm"] { background-color: #eecbff; padding: 20px; border-radius: 15px; border: 2px solid #b4a7d6; }
</style>
""", unsafe_allow_html=True)

st.title("🧙‍♂️ The Alchemist's Altar")
st.markdown("### Balance the equation step-by-step to isolate x.")

# --- 2. INITIALIZE SPELL (Session State) ---
x = sp.Symbol('x') 

if 'puzzle_lhs' not in st.session_state:
    a = random.randint(2, 5)
    target_x = random.randint(1, 9)
    b = random.randint(1, 10)
    c = (a * target_x) + b
    
    st.session_state.puzzle_lhs = a * x + b
    st.session_state.puzzle_rhs = sp.Integer(c)
    st.session_state.puzzle_solution = target_x
    st.session_state.puzzle_solved = False

# --- 3. CHECK FOR VICTORY FIRST ---
if not st.session_state.puzzle_solved:
    # If the left side is just 'x' and the right side is the answer, they win!
    if st.session_state.puzzle_lhs == x and st.session_state.puzzle_rhs == st.session_state.puzzle_solution:
        st.session_state.puzzle_solved = True

# --- 4. RENDER THE GAME ---
if st.session_state.puzzle_solved:
    st.success(f"VICTORY! The equation is balanced. x = {st.session_state.puzzle_solution} (｡◕‿◕｡)━☆ﾟ.*･｡ﾟ")
    if st.button("Generate New Spell"):
        del st.session_state.puzzle_lhs
        st.rerun()

else:
    # Scry the current state of the equation
    st.markdown(f'<div class="equation-container"><span class="equation-text">${sp.latex(st.session_state.puzzle_lhs)} = {sp.latex(st.session_state.puzzle_rhs)}$</span></div>', unsafe_allow_html=True)

    # The Alchemist's Tools
    st.write("### Choose Your Balancing Spell")

    with st.form("balancing_act"):
        op = st.selectbox("Select Operation", ["Add (+)", "Subtract (-)", "Multiply (×)", "Divide (÷)"])
        value_raw = st.text_input("Enter Value")
        apply_magic = st.form_submit_button("🧪 Apply Balancing Spell!")

    if apply_magic and value_raw:
        magic_success = False
        try:
            # Parse the value
            mod_val = sp.sympify(value_raw)
            current_lhs = st.session_state.puzzle_lhs
            current_rhs = st.session_state.puzzle_rhs
            
            # Apply the math
            if op == "Add (+)":
                new_lhs, new_rhs = current_lhs + mod_val, current_rhs + mod_val
            elif op == "Subtract (-)":
                new_lhs, new_rhs = current_lhs - mod_val, current_rhs - mod_val
            elif op == "Multiply (×)":
                new_lhs, new_rhs = current_lhs * mod_val, current_rhs * mod_val
            elif op == "Divide (÷)":
                if mod_val == 0:
                    st.error("The magic backfires! Cannot divide by zero.")
                    st.stop()
                new_lhs, new_rhs = current_lhs / mod_val, current_rhs / mod_val

            # Store the simplified equations
            st.session_state.puzzle_lhs = sp.simplify(new_lhs)
            st.session_state.puzzle_rhs = sp.simplify(new_rhs)
            magic_success = True

        except Exception: # <-- This specific exception trap fixes the bug!
            st.error("Invalid arcane value! Use numbers only.")
            
        if magic_success:
            st.rerun()
