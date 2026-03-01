import streamlit as st
import random
import pandas as pd
import math
import time
import datetime
import numpy as np
import plotly.graph_objects as go 
import streamlit.components.v1 as components 
from streamlit_gsheets import GSheetsConnection

# --- 1. SETTINGS & THEMING ---
st.set_page_config(page_title="Sorcery Sums", page_icon="🪄", layout="centered")

# Initialize Session States
if "app_stage" not in st.session_state:
    st.session_state.app_stage = "login"

# Autorefresh for Leaderboard
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=30000, key="datarefresh")
except:
    pass

# Determine the main magic button asset based on stage using your original working links
if st.session_state.app_stage == "login":
    button_image = "https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/enterrealm.png"
else:
    button_image = "https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/castspell.png"

st.markdown(f"""
    <style>
    /* 1. Main Background */
    .stApp {{ background-color: #f2e2ff; }}
    
    /* 2. Sidebar Background */
    [data-testid="stSidebar"] {{
        background-color: #ddfffc !important;
        border-right: 2px solid #c6c7ff;
    }}

    /* 3. WHITE GRAPH BACKGROUND FIX */
    div[data-testid="stChart"] {{
        background-color: white !important; padding: 10px; border-radius: 10px; border: 2px solid #7b7dbd;
    }}

    /* 4. PERIWINKLE CRYSTAL BALL FONT */
    .stExpander {{ background-color: rgba(255, 255, 255, 0.5); border-radius: 15px; }}
    .stExpander p, .stExpander span, .stExpander label {{ color: #7b7dbd !important; font-weight: bold; }}

    /* 5. YELLOW SUCCESS BOX FONT FIX */
    .success-box {{
        background-color: #ffffe3; border: 3px solid #b4a7d6; border-radius: 20px; 
        padding: 20px; text-align: center; margin-top: 15px; margin-bottom: 15px;
    }}
    .success-box h2 {{ color: #f2e2ff !important; text-shadow: 1px 1px 2px #7b7dbd; margin: 0; font-size: 24px; }}

    /* 6. GLOBAL SIDEBAR TEXT */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label p {{
        color: #7b7dbd !important;
    }}

    /* --- INVISIBLE BEACONS: HIDE THE MARKERS --- */
    div[data-testid="stElementContainer"]:has(.beacon), 
    div.element-container:has(.beacon) {{
        display: none !important;
    }}
    /* --- THE RECTANGULAR & MAGIC BUTTON BASE --- */
    
    /* 1. Remove max-width from the Streamlit wrapper div */
    div[data-testid="stElementContainer"]:has(.beacon) + div,
    div.element-container:has(.beacon) + div {{
        max-width: none !important;
    }}

    /* 2. Style the actual buttons to break out of the columns */
    div[data-testid="stElementContainer"]:has(.beacon) + div button,
    div.element-container:has(.beacon) + div button {{
        background-color: transparent !important;
        border: none !important;
        color: transparent !important;
        background-size: contain !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        width: 1400% !important;       /* Expand beyond the tight column */
        max-width: none !important;   /* YOUR TRICK: Force it to ignore limits */
        margin-left: -160% !important; /* Perfectly center the oversized button */
        height: 110px !important;     /* Adjusted to fit the wider aspect ratio */
        box-shadow: none !important;
        transition: transform 0.2s ease;
        display: block !important;
    }}
    
    div[data-testid="stElementContainer"]:has(.beacon) + div button p,
    div.element-container:has(.beacon) + div button p {{
        display: none !important;
    }}

    div[data-testid="stElementContainer"]:has(.beacon) + div button:hover,
    div.element-container:has(.beacon) + div button:hover {{
        transform: scale(1.08); /* Slightly larger hover pop */

    }}

    /* --- MAP THE EXACT IMAGES TO THE BEACON IDs --- */
    /* Algebra */
    div.element-container:has(#alg10) + div button, div[data-testid="stElementContainer"]:has(#alg10) + div button {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/algebra10.png") !important; }}
    div.element-container:has(#alg11) + div button, div[data-testid="stElementContainer"]:has(#alg11) + div button {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/algebra11.png") !important; }}
    div.element-container:has(#alg12) + div button, div[data-testid="stElementContainer"]:has(#alg12) + div button {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/algebra12.png") !important; }}

    /* Quadratics */
    div.element-container:has(#quad10) + div button, div[data-testid="stElementContainer"]:has(#quad10) + div button {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/quadratics10.png") !important; }}
    div.element-container:has(#quad11) + div button, div[data-testid="stElementContainer"]:has(#quad11) + div button {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/quadratics11.png") !important; }}
    div.element-container:has(#quad12) + div button, div[data-testid="stElementContainer"]:has(#quad12) + div button {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/quadratics12.png") !important; }}

    /* Functions */
    div.element-container:has(#func10) + div button, div[data-testid="stElementContainer"]:has(#func10) + div button {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/function10.png") !important; }}
    div.element-container:has(#func11) + div button, div[data-testid="stElementContainer"]:has(#func11) + div button {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/functions11.png") !important; }}
    div.element-container:has(#func12) + div button, div[data-testid="stElementContainer"]:has(#func12) + div button {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/functions12.png") !important; }}

    /* Geometry */
    div.element-container:has(#geo10) + div button, div[data-testid="stElementContainer"]:has(#geo10) + div button {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/geometry10.png") !important; }}
    div.element-container:has(#geo11) + div button, div[data-testid="stElementContainer"]:has(#geo11) + div button {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/geometry11.png") !important; }}
    div.element-container:has(#geo12) + div button, div[data-testid="stElementContainer"]:has(#geo12) + div button {{ background-image: url("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/geometry12.png") !important; }}

    /* --- THE BIG MAGIC BUTTONS (Enter Realm / Cast Spell) --- */
    div.element-container:has(#magic_btn) + div button, div[data-testid="stElementContainer"]:has(#magic_btn) + div button {{
        background-image: url("{button_image}") !important;
        width: 275px !important;
        height: 300px !important;
        margin: -120px auto 0 auto !important; 
    }}

    /* 8. NEW COMBINED HEADER POSITIONING */
    div[data-testid="stImage"] {{ margin-bottom: -45px; overflow: visible !important; }}
    img[src*="1000037180"], img[src*="sorcerersums.png"] {{
        width: 140% !important; max-width: none !important;
        transform: scale(1.05); display: block !important;
        margin-left: -20% !important; margin-bottom: -40px !important;
    }}

    /* Selection Page Title Tweaks */
    img[src*="schoolstudy.png"] {{
        width: 100% !important; max-width: 100% !important;
        transform: none !important; margin-left: 0 !important; margin-bottom: 10px !important;
    }}

    /* 9. PULL THE NAME PLATE UP INTO THE CLOUDS */
    div[data-testid="stTextInput"] {{ margin-top: 30px; position: relative; z-index: 10; }}

    /* 11. Question Container Styling */
    .question-container {{
        background-color: white; padding: 30px; border-radius: 20px; 
        border: 4px solid #c6c7ff; text-align: center; margin-bottom: 20px; margin-top: 60px;
    }}
    .question-container h1, .question-container h3 {{ color: #7b7dbd !important; }}

    /* THE MAGIC KEYFRAMES */
    @keyframes floatUp {{
        0% {{ transform: translateY(0) rotate(0deg); opacity: 1; }}
        100% {{ transform: translateY(-110vh) rotate(360deg); opacity: 0; }}
    }}

    div[data-testid="stTextArea"] textarea {{ background-color: #b4a7d6 !important; color: #d4ffea !important; border-radius: 10px; }}
    div[data-testid="stTextInput"] input {{ background-color: #e6fff8 !important; color: #7b7dbd !important; text-align: center; }}
       
    .block-container {{ max-width: 800px !important; padding-top: 2rem; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE SACRED STAR EFFECT ---
def pastel_star_effect():
    components.html(f"""
    <script>
    const colors = ["#ffd6ff","#caffbf","#fdffb6","#bdb2ff","#a0c4ff"];
    for (let i = 0; i < 30; i++) {{
        let star = window.parent.document.createElement("div");
        star.style.position = "fixed";
        star.style.width = "25px";
        star.style.height = "25px";
        star.style.clipPath = "polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)";
        star.style.left = Math.random() * 100 + "vw";
        star.style.top = "100vh"; 
        star.style.background = colors[Math.floor(Math.random() * colors.length)];
        star.style.zIndex = "10000";
        star.style.pointerEvents = "none";
        star.style.animation = "floatUp 2.5s ease-out forwards";
        window.parent.document.body.appendChild(star);
        setTimeout(() => star.remove(), 2500);
    }}
    </script>
    """, height=0)

# --- 3. DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 4. MATH LOGIC ---
def generate_spell(unit, level):
    prog = int(level) - 9 
    fig = None
    
    def apply_sacred_style(fig):
        fig.update_layout(
            plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=True, zerolinecolor='black'),
            yaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=True, zerolinecolor='black'),
            height=400
        )
        return fig

    if "Algebra" in unit:
        a = random.randint(2, 5 * prog)
        b = random.randint(1, 10 * prog)
        x = random.randint(1, 12)
        c = (a * x) + b
        image_tag = f"Imagine a balance scale. Side A: {a} mystery boxes (x) + {b} gems. Side B: {c} gems."
        return f"Solve for x: {a}x + {b} = {c}", x, image_tag, None

    elif "Quadratics" in unit:
        h, k = random.randint(-3, 3), random.randint(1, 5)
        x_vals = np.linspace(h-5, h+5, 100)
        y_vals = (x_vals - h)**2 + k
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='black', width=3), name="Spell Path"))
        fig = apply_sacred_style(fig)
        image_tag = "Hover to scry the point! Locate the vertex (the lowest point of the curve)."
        return f"Find the vertex y-coordinate:", k, image_tag, fig

    elif "Functions" in unit:
        m = random.randint(1, 3); b_val = random.randint(-2, 2)
        target_x = random.randint(-2, 2); ans = m * target_x + b_val
        x_vals = np.linspace(-10, 10, 100)
        y_vals = m * x_vals + b_val
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='black', width=3), name="Function"))
        fig = apply_sacred_style(fig)
        image_tag = f"Follow the line to x = {target_x} and scry the corresponding y value."
        return f"Using the crystal aid, find f({target_x})", ans, image_tag, fig

    elif "Geometry" in unit:
        side = random.randint(3, 7 * prog)
        if level == "12":
            ans = side**3
            return f"The side of a cube is {side}. Find Volume.", ans, f"A 3D cube with side {side}.", None
        ans = side * 4
        return f"A square has a side of {side}. Find Perimeter.", ans, f"A square with side {side}.", None
    
    return "Scroll not found", 0, "", None


# --- GLOBALLY RENDER LEADERBOARD IN SIDEBAR (If not logging in) ---
if st.session_state.app_stage != "login":
    st.sidebar.markdown("---")
    st.sidebar.markdown("# 🏆 Hall of Wizards")
    try:
        scores_df = conn.read(ttl=0)
        if not scores_df.empty:
            scores_df['Date'] = pd.to_datetime(scores_df['Date'])
            now = datetime.datetime.now()
            t1, t2, t3 = st.sidebar.tabs(["Week", "Month", "Year"])
            with t1:
                w_data = scores_df[scores_df['Date'] >= (now - datetime.timedelta(days=7))]
                if not w_data.empty: st.table(w_data.groupby("Name")["Score"].sum().sort_values(ascending=False).astype(int))
    except:
        st.sidebar.write("The scrolls are sleeping.")


# --- STAGE 1: LOGIN SCREEN ---
if st.session_state.app_stage == "login":
    try:
        # Reverted back to your original local logo file
        st.image("sorcerersums.png", use_container_width=False)
    except:
        st.write("✨ **Portal Opening...** ✨")
    
    name = st.text_input("", placeholder="Type your name here...", label_visibility="collapsed")

    # Drop the beacon right before the button so the CSS finds it!
    st.markdown('<div class="beacon" id="magic_btn"></div>', unsafe_allow_html=True)
    
    if st.button("Enter Realm"):
        if name:
            st.session_state.player_name = name
            st.session_state.app_stage = "selection"
            st.rerun()

# --- STAGE 2: SUBJECT SELECTION (The 12 Rectangles with Beacons) ---
elif st.session_state.app_stage == "selection":
    
    # Render the exact Title Image using the Raw URL
    st.image("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/schoolstudy.png")
    
    # Render the 4x3 Grid
    subjects = [("Algebra", "alg"), ("Quadratics", "quad"), ("Functions", "func"), ("Geometry", "geo")]
    
    st.write("") # Spacing

    for label, sub_key in subjects:
        # THE SUBJECT TITLES ARE GONE!
        cols = st.columns(3)
        for i, grade in enumerate(["10", "11", "12"]):
            beacon_id = f"{sub_key}{grade}"
            
            with cols[i]:
                # 1. Drop the invisible HTML beacon
                st.markdown(f'<div class="beacon" id="{beacon_id}"></div>', unsafe_allow_html=True)
                
                # 2. Render the Streamlit button immediately after it
                # We use a unique key so Streamlit doesn't get confused by multiple buttons
                if st.button(f"{label} {grade}", key=f"btn_{beacon_id}"):
                    st.session_state.unit_choice = label
                    st.session_state.level_choice = grade
                    # Generate the very first question
                    q, ans, img, pdf = generate_spell(label, grade)
                    st.session_state.current_q, st.session_state.target_ans = q, ans
                    st.session_state.current_image, st.session_state.current_plot = img, pdf
                    st.session_state.app_stage = "game"
                    st.rerun()


# --- STAGE 3: THE MAIN GAME ---
elif st.session_state.app_stage == "game":
    
    # Add a back button to the sidebar
    st.sidebar.title("📜 Choose Your Scroll")
    if st.sidebar.button("⬅️ Change Subject"):
        st.session_state.app_stage = "selection"
        st.rerun()

    # Reverted back to your original local file name
    try:
        st.image("Sorcery Sums.png")
    except:
        st.title("Sorcery Sums")

    st.markdown(f"""
        <div class="question-container">
            <h3>Grade {st.session_state.level_choice} {st.session_state.unit_choice}</h3>
            <h1>{st.session_state.current_q}</h1>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("🔮 Peer into the Crystal Ball (Visual Aid)"):
        st.write(st.session_state.get('current_image', 'No visual found.'))
        if st.session_state.current_plot is not None:
            st.plotly_chart(st.session_state.current_plot, use_container_width=True, config={'displayModeBar': False})

    st.text_area("Spellbook Scratchpad:", placeholder="Work out equations...", height=100, key="scratchpad")
    user_ans_raw = st.text_input("Your Final Answer:", placeholder="Type number here...", key="user_answer")

    # Drop the beacon right before the Cast Spell button
    st.markdown('<div class="beacon" id="magic_btn"></div>', unsafe_allow_html=True)

    if st.button("🪄 Cast Spell!"):
        try:
            if math.isclose(float(user_ans_raw), st.session_state.target_ans, rel_tol=0.1):
                pastel_star_effect()
                st.markdown('<div class="success-box"><h2>Correct! (｡◕‿◕｡)━☆ﾟ.*･｡ﾟ</h2></div>', unsafe_allow_html=True)
                time.sleep(.2) 
                try:
                    df = conn.read(ttl=0)
                    new_row = pd.DataFrame([{"Name": st.session_state.player_name, "Score": 50, "Date": datetime.datetime.now().strftime("%Y-%m-%d")}])
                    conn.update(data=pd.concat([df, new_row], ignore_index=True))
                except: pass
                
                q, ans, img, pdf = generate_spell(st.session_state.unit_choice, st.session_state.level_choice)
                st.session_state.current_q, st.session_state.target_ans = q, ans
                st.session_state.current_image, st.session_state.current_plot = img, pdf
                st.rerun()
            else: st.error("The magic failed!")
        except: st.warning("Enter a number!")

