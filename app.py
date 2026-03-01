import streamlit as st

st.set_page_config(page_title="Grid Test", layout="centered")

# --- 1. THE COORDINATE CSS WITH RAW URLS ---
st.markdown("""
    <style>
    /* Global reset for all buttons INSIDE a column block */
    div[data-testid="stHorizontalBlock"] button {
        background-color: transparent !important;
        border: none !important;
        color: transparent !important;
        background-size: contain !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        width: 100% !important;
        height: 85px !important;
        box-shadow: none !important;
        transition: transform 0.2s ease;
    }
    div[data-testid="stHorizontalBlock"] button:hover { transform: scale(1.05); }
    div[data-testid="stHorizontalBlock"] button p { display: none !important; }

    /* ROW 1: ALGEBRA */
    div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-of-type(1) button { background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/algebra10.png") !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-of-type(2) button { background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/algebra11.png") !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-of-type(3) button { background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/algebra12.png") !important; }

    /* ROW 2: QUADRATICS */
    div[data-testid="stHorizontalBlock"]:nth-of-type(2) div[data-testid="column"]:nth-of-type(1) button { background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/quadratics10.png") !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(2) div[data-testid="column"]:nth-of-type(2) button { background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/quadratics11.png") !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(2) div[data-testid="column"]:nth-of-type(3) button { background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/quadratics12.png") !important; }

    /* ROW 3: FUNCTIONS (Note the singular 'function10.png' based on your list!) */
    div[data-testid="stHorizontalBlock"]:nth-of-type(3) div[data-testid="column"]:nth-of-type(1) button { background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/function10.png") !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(3) div[data-testid="column"]:nth-of-type(2) button { background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/functions11.png") !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(3) div[data-testid="column"]:nth-of-type(3) button { background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/functions12.png") !important; }

    /* ROW 4: GEOMETRY */
    div[data-testid="stHorizontalBlock"]:nth-of-type(4) div[data-testid="column"]:nth-of-type(1) button { background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/geometry10.png") !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(4) div[data-testid="column"]:nth-of-type(2) button { background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/geometry11.png") !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(4) div[data-testid="column"]:nth-of-type(3) button { background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/geometry12.png") !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE UI RENDER ---
st.image("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/schoolstudy.png")

# Render Row 1
st.markdown("### Algebra")
cols1 = st.columns(3)
if cols1[0].button("A10"): st.success("Clicked Algebra 10!")
if cols1[1].button("A11"): st.success("Clicked Algebra 11!")
if cols1[2].button("A12"): st.success("Clicked Algebra 12!")

# Render Row 2
st.markdown("### Quadratics")
cols2 = st.columns(3)
if cols2[0].button("Q10"): st.success("Clicked Quadratics 10!")
if cols2[1].button("Q11"): st.success("Clicked Quadratics 11!")
if cols2[2].button("Q12"): st.success("Clicked Quadratics 12!")

# Render Row 3
st.markdown("### Functions")
cols3 = st.columns(3)
if cols3[0].button("F10"): st.success("Clicked Functions 10!")
if cols3[1].button("F11"): st.success("Clicked Functions 11!")
if cols3[2].button("F12"): st.success("Clicked Functions 12!")

# Render Row 4
st.markdown("### Geometry")
cols4 = st.columns(3)
if cols4[0].button("G10"): st.success("Clicked Geometry 10!")
if cols4[1].button("G11"): st.success("Clicked Geometry 11!")
if cols4[2].button("G12"): st.success("Clicked Geometry 12!")
