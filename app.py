import streamlit as st

st.set_page_config(page_title="Grid Test", layout="centered")

# --- THE SACRED LAYOUT CSS ---
st.markdown("""
    <style>
    /* 1. The Pink Selection Pods */
    div[role="radiogroup"] {
        background-color: #ffdef2 !important;
        padding: 25px;
        border-radius: 15px;
        border: 3px solid #eecbff;
        margin-bottom: 15px;
    }
    
    /* 2. Pod Text Styling */
    div[role="radiogroup"] label {
        color: #7b7dbd !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }

    /* 3. Hide annoying Streamlit Header Anchor Links */
    h3 a { display: none !important; }

    /* 4. Giant 'Unroll Scroll' Button */
    button[kind="primary"] {
        background-color: #ddfffc !important;
        border: 3px solid #c6c7ff !important;
        color: #7b7dbd !important;
        font-size: 24px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        height: 70px !important;
        width: 100% !important;
        transition: transform 0.2s ease;
    }
    button[kind="primary"]:hover {
        transform: scale(1.05);
        background-color: #e6fff8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- STAGE 2: SUBJECT SELECTION ---
st.image("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/choose_subject_title.png")

st.write("") # Spacing

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📜 Select Subject")
    unit = st.radio("Subject", ["Algebra", "Quadratics", "Functions", "Geometry"], label_visibility="collapsed")

with col2:
    st.markdown("### 🎚️ Select Grade")
    level = st.radio("Grade", ["10", "11", "12"], label_visibility="collapsed")

st.write("") # Spacing

if st.button("Unroll Scroll ✨", type="primary"):
    st.success(f"Magic activated! You chose Grade {level} {unit}.")
