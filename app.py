import streamlit as st

# 1. The CSS Hack
st.markdown("""
    <style>
    /* Target the button using the invisible 'title' tag we create with help="" */
    button[title="alg10"] {
        background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/algebra10.png") !important;
        background-color: transparent !important;
        border: none !important;
        color: transparent !important; /* Hides default text */
        background-size: contain !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        width: 250px !important; /* Wide rectangle size */
        height: 85px !important;
        box-shadow: none !important;
        cursor: pointer !important;
    }
    
    /* Double-tap to ensure Streamlit's default <p> text is hidden */
    button[title="alg10"] p {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Test the Title Image
st.write("Testing Title Image:")
st.image("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/choose_subject_title.png")

# 3. Test the Invisible CSS Button
st.write("Testing CSS Rectangular Button:")
if st.button("Algebra 10", help="alg10"):
    st.success("✨ The magic button is visible and clickable! ✨")
