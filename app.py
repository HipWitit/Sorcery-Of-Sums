import streamlit as st

st.markdown("""
<style>
/* Target the button in the First Row, First Column */
div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-of-type(1) button {
    background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/algebra10.png") !important;
    background-color: transparent !important;
    border: none !important;
    color: transparent !important;
    background-size: contain !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    width: 250px !important;
    height: 85px !important;
    box-shadow: none !important;
}

div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-of-type(1) button p {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

st.write("1. Testing the Title Image URL directly:")
# Double check the exact capitalization of this file in your GitHub
st.image("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/choose_subject_title.png")

st.write("2. Testing the CSS Row/Column targeting:")
row1_cols = st.columns(3)
with row1_cols[0]:
    if st.button("Algebra 10"):
        st.success("✨ The magic button is visible and clickable! ✨")
