import streamlit as st
import random

st.title("🔢 Math Mayhem: Remote Edition")

# This is where we will eventually connect your Database
st.sidebar.header("Leaderboard")
st.sidebar.write("Player 1: 100 pts")

st.write("Welcome to the game! Ready to solve some equations?")

if st.button("Generate First Question"):
    st.write("Logic coming soon...")
