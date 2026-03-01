import streamlit as st
import random
import sympy as sp # This is the magical library that makes this work!

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
x = sp.Symbol('x') # Declare 'x' as an algebraic symbol

# Only run this once to create the puzzle
if 'puzzle_lhs' not in st.session_state:
    a = random.randint(2, 5)
    target_x = random.randint(1, 9)
    b = random.randint(1, 10)
    c = (a * target_x) + b
    
    st.session_state.puzzle_lhs = a * x + b
    st.session_state.puzzle_rhs = sp.Integer(c)
    st.session_state.puzzle_solution = target_x
    st.session_state.puzzle_solved = False

# Scry the current state of the equation
st.markdown(f'<div class="equation-container"><span class="equation-text">${sp.latex(st.session_state.puzzle_lhs)} = {sp.latex(st.session_state.puzzle_rhs)}$</span></div>', unsafe_allow_html=True)

# --- 3. THE ALCHEMIST'S TOOLS (The Interactive Part) ---
st.write("### Choose Your Balancing Spell")
tool_cols = st.columns(2)

with st.form("balancing_act"):
    op = st.selectbox("Select Operation", ["Add (+)", "Subtract (-)", "Multiply (×)", "Divide (÷)"])
    value_raw = st.text_input("Enter Value")
    apply_magic = st.form_submit_button("🧪 Apply Balancing Spell!")

if apply_magic and value_raw:
    try:
        # 1. Parse the value into a SymPy object (handles numbers and fractions)
        mod_val = sp.sympify(value_raw)
        
        # 2. Get the current equations from memory
        current_lhs = st.session_state.puzzle_lhs
        current_rhs = st.session_state.puzzle_rhs
        
        # 3. Mathematically apply the operation to BOTH sides
        if op == "Add (+)":
            new_lhs, new_rhs = current_lhs + mod_val, current_rhs + mod_val
        elif op == "Subtract (-)":
            new_lhs, new_rhs = current_lhs - mod_val, current_rhs - mod_val
        elif op == "Multiply (×)":
            new_lhs, new_rhs = current_lhs * mod_val, current_rhs * mod_val
        elif op == "Divide (÷)":
            # Avoid division by zero!
            if mod_val == 0:
                st.error("The magic backfires! Cannot divide by zero.")
                st.stop()
            new_lhs, new_rhs = current_lhs / mod_val, current_rhs / mod_val

        # 4. Store the newly simplified equations back into memory
        st.session_state.puzzle_lhs = sp.simplify(new_lhs)
        st.session_state.puzzle_rhs = sp.simplify(new_rhs)
        
        st.rerun() # Refresh to show the new equation

    except: st.error("Invalid arcane value! Use numbers only.")


# --- 4. CHECK FOR VICTORY ---
current_lhs = st.session_state.puzzle_lhs
current_rhs = st.session_state.puzzle_rhs

if st.session_state.puzzle_solved:
    st.success(f"VICTORY! The equation is balanced. x = {st.session_state.puzzle_solution} (｡◕‿◕｡)━☆ﾟ.*･｡ﾟ")
    if st.button("Generate New Spell"):
        del st.session_state.puzzle_lhs
        del st.session_state.puzzle_solved
        st.rerun()

elif current_lhs == x:
    # We found the solution!
    if current_rhs == st.session_state.puzzle_solution:
        st.session_state.puzzle_solved = True
        st.rerun()

