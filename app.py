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
import sympy as sp # Added SymPy for the Altar
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

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
        margin-left: -125% !important; /* Perfectly center the oversized button */
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

    /* Selection Page & Great Hall Title Tweaks */
    img[src*="schoolstudy.png"], img[src*="TheGH.png"], img[src*="beholdpowerful.png"] {{
        width: 100% !important; max-width: 100% !important;
        transform: none !important; margin-left: 0 !important; margin-bottom: 30px !important;
    }}

    /* 9. PULL THE NAME PLATE UP INTO THE CLOUDS */
    div[data-testid="stTextInput"] {{ margin-top: 30px; position: relative; z-index: 10; }}

    /* 10. Question Container Styling */
    .question-container {{
        background-color: white; padding: 30px; border-radius: 20px; 
        border: 4px solid #c6c7ff; text-align: center; margin-bottom: 20px; margin-top: 60px;
    }}
    .question-container h1, .question-container h3 {{ color: #7b7dbd !important; }}

    /* --- 11. ALCHEMICAL ALTAR CSS --- */
    .equation-container {{
        background-color: white; padding: 40px; border-radius: 20px; 
        border: 5px solid #c6c7ff; text-align: center; margin-top: 30px; margin-bottom: 30px;
    }}
    .equation-text {{ font-size: 40px; color: #7b7dbd !important; font-weight: bold; }}
    div[data-testid="stForm"] {{ background-color: #eecbff; padding: 20px; border-radius: 15px; border: 2px solid #b4a7d6; margin-bottom: 20px;}}


    /* THE MAGIC KEYFRAMES */
    @keyframes floatUp {{
        0% {{ transform: translateY(0) rotate(0deg); opacity: 1; }}
        100% {{ transform: translateY(-110vh) rotate(360deg); opacity: 0; }}
    }}

    div[data-testid="stTextArea"] textarea {{ background-color: #b4a7d6 !important; color: #d4ffea !important; border-radius: 10px; }}
    div[data-testid="stTextInput"] input {{ background-color: #e6fff8 !important; color: #7b7dbd !important; text-align: center; }}
       
    .block-container {{ max-width: 800px !important; padding-top: 2rem; }}
                                            
    /* --- 12. GREAT HALL LEADERBOARD TABLES --- */
    [data-testid="stTable"] {{
        background-color: white;
        border-radius: 0px;
        overflow: hidden;
        border: 3px solid #b4a7d6;
    }}
    [data-testid="stTable"] th {{
        background-color: #e2eeff !important;
        color: #7b7dbd !important;
        font-size: 18px;
        text-align: center !important;
        border-bottom: 2px solid #b4a7d6 !important;
    }}
    [data-testid="stTable"] td {{
        color: #7b7dbd !important;
        text-align: center !important;
        font-weight: bold;
    }}

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

# --- 4. MATH LOGIC WITH SYMPY ---
x_sym = sp.Symbol('x', real=True)

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
        if level == "10":
            x = random.randint(1, 12)
            c_val = random.randint(2, 5)
            a = c_val + random.randint(1, 5) 
            b = random.randint(1, 15)
            d = (a * x) + b - (c_val * x)
            lhs = a * x_sym + b
            rhs = c_val * x_sym + d
            image_tag = f"A shifting scale! {a} boxes and {b} gems balances perfectly with {c_val} boxes and {d} gems."
            return f"Balance the equation to reveal x:", x, image_tag, None, lhs, rhs
            
        elif level == "11":
            c_val = random.randint(3, 9)
            b = random.randint(1, 20)
            x = (c_val**2) - b
            lhs = sp.sqrt(x_sym + b)
            rhs = sp.Integer(c_val)
            image_tag = f"Pierce the veil! The square root of the mystery box plus {b} equals {c_val}."
            return f"Balance the equation to reveal x:", x, image_tag, None, lhs, rhs
            
        elif level == "12":
            base = random.randint(2, 4)
            a = random.randint(2, 4) 
            c_val = random.randint(1, 10)
            x = (base**a) + c_val
            lhs = sp.log(x_sym - c_val, base)
            rhs = sp.Integer(a)
            image_tag = f"Decipher the ancient logarithm! Base {base} reaches power {a} to reveal x minus {c_val}."
            return f"Balance the equation to reveal x:", x, image_tag, None, lhs, rhs

    elif "Quadratics" in unit:
        if level == "10":
            # Grade 10: Area Model (Algebra Tiles) for (x + a)(x + b)
            a = random.randint(2, 5)
            b = random.randint(2, 5)
            
            fig = go.Figure()
            
            # Your Sacred Pastel Colors
            c_green = "#d4ffea"
            c_yellow = "#ffffe3"
            c_blue = "#e4fffe"
            c_gray = "#e2eeff"
            text_color = "#7b7dbd"
            
            # 1. Top-Left Box: x² (One big 4x4 box)
            fig.add_shape(type="rect", x0=0, y0=0, x1=4, y1=4, fillcolor=c_green, line=dict(color="white", width=4), layer="below")
            fig.add_annotation(x=2, y=2, text="x²", showarrow=False, font=dict(size=24, color=text_color, weight="bold"))
            
            # 2. Top-Right Boxes: a * x (Individual vertical yellow strips)
            for i in range(a):
                fig.add_shape(type="rect", x0=4+i, y0=0, x1=5+i, y1=4, fillcolor=c_yellow, line=dict(color="white", width=4), layer="below")
                fig.add_annotation(x=4.5+i, y=2, text="x", showarrow=False, font=dict(size=18, color=text_color, weight="bold"))
                
            # 3. Bottom-Left Boxes: b * x (Individual horizontal blue strips)
            for j in range(b):
                fig.add_shape(type="rect", x0=0, y0=-1-j, x1=4, y1=-j, fillcolor=c_blue, line=dict(color="white", width=4), layer="below")
                fig.add_annotation(x=2, y=-0.5-j, text="x", showarrow=False, font=dict(size=18, color=text_color, weight="bold"))
                
            # 4. Bottom-Right Boxes: a * b (Individual grey unit squares!)
            for i in range(a):
                for j in range(b):
                    fig.add_shape(type="rect", x0=4+i, y0=-1-j, x1=5+i, y1=-j, fillcolor=c_gray, line=dict(color="white", width=4), layer="below")
            
            # The Giant Mystery Question Mark floating over the grey grid
            fig.add_annotation(x=4+(a/2), y=-(b/2), text="?", showarrow=False, font=dict(size=40, color=text_color, weight="bold"))
            
            # Outside Labels (The lengths of the sides)
            fig.add_annotation(x=2, y=4.6, text="x", showarrow=False, font=dict(size=22, color=text_color, weight="bold"))
            fig.add_annotation(x=4+(a/2), y=4.6, text=f"+ {a}", showarrow=False, font=dict(size=22, color=text_color, weight="bold"))
            fig.add_annotation(x=-0.8, y=2, text="x", showarrow=False, font=dict(size=22, color=text_color, weight="bold"))
            fig.add_annotation(x=-0.8, y=-(b/2), text=f"+ {b}", showarrow=False, font=dict(size=22, color=text_color, weight="bold"))
            
            # Lock the view so the blocks perfectly scale
            fig.update_layout(
                xaxis=dict(visible=False, range=[-1.5, 5.5+a]),
                yaxis=dict(visible=False, range=[-1.5-b, 5.5]),
                margin=dict(l=0, r=0, t=0, b=0),
                plot_bgcolor='white', paper_bgcolor='white',
                height=380
            )
            
            ans = a * b
            image_tag = "Count the tiles! Scry the total number of small grey boxes."
            return f"Multiply (x + {a})(x + {b}). What is the value of the grey area?", ans, image_tag, fig, None, None
            
        elif level == "11":
            # Grade 11: Vertex form (Interactive Graph)
            h, k = random.randint(-3, 3), random.randint(1, 5)
            x_vals = np.linspace(h-5, h+5, 100)
            y_vals = (x_vals - h)**2 + k
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='black', width=3), name="Spell Path"))
            fig = apply_sacred_style(fig)
            
            h_str = f"- {h}" if h > 0 else (f"+ {abs(h)}" if h < 0 else "")
            eq_str = f"y = (x {h_str})² + {k}" if h != 0 else f"y = x² + {k}"
            
            image_tag = "Hover to scry the point! Locate the vertex (the lowest point of the curve)."
            return f"Given {eq_str}, find the vertex y-coordinate:", k, image_tag, fig, None, None

        elif level == "12":
            # Grade 12: The Discriminant (b² - 4ac)
            a = random.randint(1, 3)
            b = random.randint(-5, 5)
            c = random.randint(-5, 5)
            ans = (b**2) - (4 * a * c)
            
            b_str = f"- {abs(b)}x " if b < 0 else (f"+ {b}x " if b > 0 else "")
            c_str = f"- {abs(c)}" if c < 0 else (f"+ {c}" if c > 0 else "")
            eq_string = f"{a}x² {b_str}{c_str}".strip() + " = 0"
            
            image_tag = "Consult the discriminant (b² - 4ac) to predict the spell's nature!"
            return f"Calculate the discriminant of {eq_string}", ans, image_tag, None, None, None


    elif "Functions" in unit:
        m = random.randint(1, 3); b_val = random.randint(-2, 2)
        target_x = random.randint(-2, 2); ans = m * target_x + b_val
        x_vals = np.linspace(-10, 10, 100)
        y_vals = m * x_vals + b_val
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='black', width=3), name="Function"))
        fig = apply_sacred_style(fig)
        image_tag = f"Follow the line to x = {target_x} and scry the corresponding y value."
        return f"Using the crystal aid, find f({target_x})", ans, image_tag, fig, None, None

    elif "Geometry" in unit:
        side = random.randint(3, 7 * prog)
        if level == "12":
            ans = side**3
            return f"The side of a cube is {side}. Find Volume.", ans, f"A 3D cube with side {side}.", None, None, None
        ans = side * 4
        return f"A square has a side of {side}. Find Perimeter.", ans, f"A square with side {side}.", None, None, None
    
    return "Scroll not found", 0, "", None, None, None


# --- GLOBAL NAVIGATION SIDEBAR (If not logging in) ---
if st.session_state.app_stage != "login":
    st.sidebar.markdown("### 🗺️ Realm Map")
    
    # If they are NOT in the Great Hall, show the portal to go there
    if st.session_state.app_stage != "great_hall":
        if st.sidebar.button("🏆 The Great Hall"):
            # Remember where they were so we can send them back!
            st.session_state.previous_stage = st.session_state.app_stage
            st.session_state.app_stage = "great_hall"
            st.rerun()
            
    # If they ARE in the Great Hall, show a button to go back to the scrolls
    else:
        if st.sidebar.button("⬅️ Return to Realm"):
            st.session_state.app_stage = st.session_state.get("previous_stage", "selection")
            st.rerun()
    st.sidebar.markdown("---")


# --- STAGE 1: LOGIN SCREEN ---
if st.session_state.app_stage == "login":
    try:
        # Dropped the deprecated use_container_width warning here!
        st.image("sorcerersums.png")
    except:
        st.write("✨ **Portal Opening...** ✨")
    
    # Patched the label warning by adding "Player Name"
    name = st.text_input("Player Name", placeholder="Type your name here...", label_visibility="collapsed")

    # Drop the beacon right before the button so the CSS finds it!
    st.markdown('<div class="beacon" id="magic_btn"></div>', unsafe_allow_html=True)
    
    if st.button("Enter Realm"):
        if name:
            st.session_state.player_name = name
            st.session_state.app_stage = "selection"
            st.rerun()

# --- STAGE 2: SUBJECT SELECTION (The 12 Rectangles with Beacons) ---
elif st.session_state.app_stage == "selection":
    
    st.image("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/59bba3415a91b29eaced863600dde0c807bd6a7a/assets/images/schoolstudy.png")
    
    # Render the 4x3 Grid
    subjects = [("Algebra", "alg"), ("Quadratics", "quad"), ("Functions", "func"), ("Geometry", "geo")]
    
    st.write("") # Spacing

    for label, sub_key in subjects:
        cols = st.columns(3)
        for i, grade in enumerate(["10", "11", "12"]):
            beacon_id = f"{sub_key}{grade}"
            
            with cols[i]:
                st.markdown(f'<div class="beacon" id="{beacon_id}"></div>', unsafe_allow_html=True)
                
                if st.button(f"{label} {grade}", key=f"btn_{beacon_id}"):
                    st.session_state.unit_choice = label
                    st.session_state.level_choice = grade
                    q, ans, img, pdf, lhs, rhs = generate_spell(label, grade)
                    st.session_state.current_q, st.session_state.target_ans = q, ans
                    st.session_state.current_image, st.session_state.current_plot = img, pdf
                    
                    st.session_state.puzzle_lhs = lhs
                    st.session_state.puzzle_rhs = rhs
                    
                    st.session_state.app_stage = "game"
                    st.rerun()


# --- STAGE 3: THE MAIN GAME ---
elif st.session_state.app_stage == "game":
    
    st.sidebar.title("📜 Choose Your Scroll")
    if st.sidebar.button("⬅️ Change Subject"):
        st.session_state.app_stage = "selection"
        st.rerun()

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
            # Fixed the deprecation warning by converting to width='stretch'
            st.plotly_chart(st.session_state.current_plot, width="stretch", config={'displayModeBar': False})

    # --- ALCHEMICAL ALTAR (For Algebra Only) ---
    if st.session_state.unit_choice == "Algebra":
        
        # 1. Victory Check
        if st.session_state.puzzle_lhs == x_sym and st.session_state.puzzle_rhs == st.session_state.target_ans:
            pastel_star_effect()
            st.markdown('<div class="success-box"><h2>Correct! The equation is balanced! (｡◕‿◕｡)━☆ﾟ.*･｡ﾟ</h2></div>', unsafe_allow_html=True)
            time.sleep(1.5) 
            try:
                df = conn.read(ttl=0)
                new_row = pd.DataFrame([{"Name": st.session_state.player_name, "Score": 50, "Date": datetime.datetime.now().strftime("%Y-%m-%d")}])
                conn.update(data=pd.concat([df, new_row], ignore_index=True))
            except:
                pass
            
            # Auto-Generate Next
            q, ans, img, pdf, lhs, rhs = generate_spell(st.session_state.unit_choice, st.session_state.level_choice)
            st.session_state.current_q, st.session_state.target_ans = q, ans
            st.session_state.current_image, st.session_state.current_plot = img, pdf
            st.session_state.puzzle_lhs, st.session_state.puzzle_rhs = lhs, rhs
            st.rerun()

        # 2. Render Altar
        st.markdown(f'<div class="equation-container"><span class="equation-text">${sp.latex(st.session_state.puzzle_lhs)} = {sp.latex(st.session_state.puzzle_rhs)}$</span></div>', unsafe_allow_html=True)
        
        with st.form("balancing_act"):
            op = st.selectbox("Select Operation", ["Add (+)", "Subtract (-)", "Multiply (×)", "Divide (÷)", "Power (^)", "Apply Base (b^x)"])
            
            # Now properly accepts 'x' variables!
            value_raw = st.text_input("Enter Arcane Value", placeholder="e.g., 5 or 5x", label_visibility="collapsed")
            apply_magic = st.form_submit_button("🧪 Apply Balancing Spell!")
            
        if apply_magic and value_raw:
            magic_success = False
            try:
                transformations = standard_transformations + (implicit_multiplication_application,)
                mod_val = parse_expr(value_raw, local_dict={'x': x_sym}, transformations=transformations)
                
                curr_lhs = st.session_state.puzzle_lhs
                curr_rhs = st.session_state.puzzle_rhs
                
                if op == "Add (+)": new_lhs, new_rhs = curr_lhs + mod_val, curr_rhs + mod_val
                elif op == "Subtract (-)": new_lhs, new_rhs = curr_lhs - mod_val, curr_rhs - mod_val
                elif op == "Multiply (×)": new_lhs, new_rhs = curr_lhs * mod_val, curr_rhs * mod_val
                elif op == "Divide (÷)":
                    if mod_val == 0: st.stop()
                    new_lhs, new_rhs = curr_lhs / mod_val, curr_rhs / mod_val
                elif op == "Power (^)":
                    new_lhs, new_rhs = curr_lhs ** mod_val, curr_rhs ** mod_val
                elif op == "Apply Base (b^x)":
                    new_lhs, new_rhs = mod_val ** curr_lhs, mod_val ** curr_rhs
                
                st.session_state.puzzle_lhs = sp.simplify(new_lhs)
                st.session_state.puzzle_rhs = sp.simplify(new_rhs)
                magic_success = True
            except Exception:
                st.error("Invalid arcane value! Use numbers or 'x' terms (e.g., 5, -2, 3x).")
                
            if magic_success: st.rerun()

    # --- STANDARD INPUT (For Non-Algebra Units) ---
    else:
        st.text_area("Spellbook Scratchpad:", placeholder="Work out equations...", height=100, key="scratchpad")
        # Patched the label warning here too
        user_ans_raw = st.text_input("Your Final Answer", placeholder="Type number here...", key="user_answer", label_visibility="collapsed")

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
                    except:
                        pass
                    
                    q, ans, img, pdf, lhs, rhs = generate_spell(st.session_state.unit_choice, st.session_state.level_choice)
                    st.session_state.current_q, st.session_state.target_ans = q, ans
                    st.session_state.current_image, st.session_state.current_plot = img, pdf
                    st.rerun()
                else: st.error("The magic failed!")
            except: st.warning("Enter a number!")


# --- STAGE 4: THE HALL OF GREAT WITCHES AND WIZARDS ---
elif st.session_state.app_stage == "great_hall":
    try:
        # 1. Main Great Hall Banner
        st.image("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/TheGH.png")
    except:
        st.markdown("<h1 style='text-align: center; color: #7b7dbd;'>🏆 The Hall Of Great Witches And Wizards</h1>", unsafe_allow_html=True)
        
    try:
        # 2. Your NEW "Behold" Scroll Image!
        st.image("https://raw.githubusercontent.com/HipWitit/Sorcery-Of-Sums/main/assets/images/beholdpowerful.png", use_container_width=True)
    except Exception as e:
        # If the image isn't on GitHub yet, show a red warning so we know why!
        st.markdown("<p style='text-align: center; color: red; font-weight: bold;'>⚠️ Waiting for beholdpowerful.png to be uploaded to GitHub...</p>", unsafe_allow_html=True)
    
    st.write("") 
    
    try:
        scores_df = conn.read(ttl=0)
        if not scores_df.empty:
            scores_df['Date'] = pd.to_datetime(scores_df['Date'])
            now = datetime.datetime.now()
            t1, t2, t3 = st.tabs(["This Week", " This Month", " All Time"])
            
            with t1:
                w_data = scores_df[scores_df['Date'] >= (now - datetime.timedelta(days=7))]
                if not w_data.empty: st.table(w_data.groupby("Name")["Score"].sum().sort_values(ascending=False).astype(int))
                else: st.info("The scrolls are blank this week.")
            
            with t2:
                m_data = scores_df[scores_df['Date'] >= (now - datetime.timedelta(days=30))]
                if not m_data.empty: st.table(m_data.groupby("Name")["Score"].sum().sort_values(ascending=False).astype(int))
                else: st.info("The scrolls are blank this month.")
                    
            with t3:
                st.table(scores_df.groupby("Name")["Score"].sum().sort_values(ascending=False).astype(int))
    except:
        st.error("The Hall's magic is currently sleeping (Database error).")

