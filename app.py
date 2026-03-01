import streamlit as st

st.set_page_config(page_title="Beacon Test", layout="centered")

st.markdown("""
    <style>
    /* 1. Hide the beacon container so it doesn't mess up your spacing */
    div[data-testid="stElementContainer"]:has(.beacon), 
    div.element-container:has(.beacon) {
        display: none !important;
    }

    /* 2. Style the button immediately following ANY beacon */
    div[data-testid="stElementContainer"]:has(.beacon) + div button,
    div.element-container:has(.beacon) + div button {
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
    
    div[data-testid="stElementContainer"]:has(.beacon) + div button p,
    div.element-container:has(.beacon) + div button p {
        display: none !important;
    }

    div[data-testid="stElementContainer"]:has(.beacon) + div button:hover,
    div.element-container:has(.beacon) + div button:hover {
        transform: scale(1.05);
    }

    /* 3. Map the exact images using the specific beacon IDs */
    div.element-container:has(#alg10) + div button, div[data-testid="stElementContainer"]:has(#alg10) + div button { 
        background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/algebra10.png") !important; 
    }
    div.element-container:has(#alg11) + div button, div[data-testid="stElementContainer"]:has(#alg11) + div button { 
        background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/algebra11.png") !important; 
    }
    div.element-container:has(#alg12) + div button, div[data-testid="stElementContainer"]:has(#alg12) + div button { 
        background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/algebra12.png") !important; 
    }
    </style>
""", unsafe_allow_html=True)

# Title Image
st.image("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/choose_subject_title.png")

# Render Row 1: Algebra
cols = st.columns(3)

with cols[0]:
    # Drop the invisible beacon right before the button
    st.markdown('<div class="beacon" id="alg10"></div>', unsafe_allow_html=True)
    if st.button("Algebra 10"):
        st.success("Algebra 10 Magic Works!")

with cols[1]:
    st.markdown('<div class="beacon" id="alg11"></div>', unsafe_allow_html=True)
    if st.button("Algebra 11"):
        st.success("Algebra 11 Magic Works!")

with cols[2]:
    st.markdown('<div class="beacon" id="alg12"></div>', unsafe_allow_html=True)
    if st.button("Algebra 12"):
        st.success("Algebra 12 Magic Works!")
