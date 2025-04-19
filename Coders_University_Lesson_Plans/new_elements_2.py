import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time
import plotly.express as px
import base64
import os
import matplotlib.pyplot as plt
import secrets

# Set page config
st.set_page_config(layout="wide", page_title="Streamlit Scavenger Hunt", page_icon="🔍")

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
        color: black;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main h1, .main h2, .main h3, .main p, .main label, .main .stMarkdown {
        color: black !important;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #ff4b4b;
        border: none;
    }
    [data-testid="stSidebar"] {
        margin-top: 45px;
        color: white;
    }
    [data-testid="stMetricDelta"] {
        display: none;
    }
    .stAlert {
        color: black;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'questions_asked' not in st.session_state:
    st.session_state.questions_asked = 0
if 'current_element' not in st.session_state:
    st.session_state.current_element = None

# Define the elements
elements = [
    ("st.latex", "Renders LaTeX expressions", lambda: st.latex(r'''e^{i\pi} + 1 = 0''')),
    ("st.code", "Displays code with syntax highlighting", lambda: st.code("def hello_world():\n    print('Hello, World!')", language="python")),
    ("st.dataframe", "Displays an interactive dataframe", lambda: st.dataframe(pd.DataFrame(np.random.randn(10, 5), columns=('col %d' % i for i in range(5))))),
    ("st.table", "Displays a static table", lambda: st.table(pd.DataFrame(np.random.randn(5, 3), columns=['a', 'b', 'c']))),
    ("st.metric", "Displays a metric in a box", lambda: st.metric(label="Temperature", value="70 °F", delta="1.2 °F")),
    ("st.line_chart", "Displays a line chart", lambda: st.line_chart(pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c']))),
    ("st.echo", "Displays code and its output", lambda: st.echo()(print)("Hello, World!")),
    ("st.caption", "Displays smaller, muted text", lambda: st.caption("This is a caption")),
    ("st.json", "Displays JSON-formatted data", lambda: st.json({"foo": "bar", "baz": "boz"})),
    ("st.image", "Displays an image", lambda: st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)),
    ("st.audio", "Displays an audio player", lambda: st.audio("https://upload.wikimedia.org/wikipedia/commons/c/c4/Muriel-Nguyen-Xuan-Chopin-valse-opus64-1.ogg")),
    ("st.video", "Displays a video player", lambda: st.video("https://youtu.be/B2iAodr0fOo")),
    ("st.map", "Displays a map", lambda: st.map(pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon']))),
    ("st.color_picker", "Displays a color picker", lambda: st.color_picker("Pick a color", "#00f900")),
    ("st.expander", "Creates an expandable container", lambda: st.expander("Expand me!").write("This is hidden until expanded.")),
    ("st.spinner", "Displays a loading spinner", lambda: st.spinner("Loading...")),
    ("st.progress", "Displays a progress bar", lambda: st.progress(0.75)),
    ("st.error", "Displays an error message", lambda: st.error("This is an error message")),
    ("st.warning", "Displays a warning message", lambda: st.warning("This is a warning message")),
    ("st.info", "Displays an informational message", lambda: st.info("This is an informational message")),
    ("st.success", "Displays a success message", lambda: st.success("This is a success message")),
    ("st.altair_chart (scatter)", "Displays an interactive Altair scatter plot", lambda: st.altair_chart(alt.Chart(pd.DataFrame(np.random.randn(50, 2), columns=['x', 'y'])).mark_circle().encode(x='x', y='y'))),
    ("st.button", "Creates a button", lambda: st.button("Click me!")),
    ("st.download_button", "Creates a download button", lambda: st.download_button("Download CSV", data="a,b,c\n1,2,3\n4,5,6", file_name="data.csv", mime="text/csv")),
    ("st.checkbox", "Creates a checkbox", lambda: st.checkbox("Check me out")),
    ("st.radio", "Creates a radio button group", lambda: st.radio("Choose one", ["Option 1", "Option 2", "Option 3"])),
    ("st.selectbox", "Creates a select box", lambda: st.selectbox("Choose an option", ["Option A", "Option B", "Option C"])),
    ("st.multiselect", "Creates a multiselect box", lambda: st.multiselect("Select multiple options", ["Red", "Green", "Blue"])),
    ("st.slider", "Creates a slider", lambda: st.slider("Select a value", 0, 100, 50)),
    ("st.select_slider", "Creates a slider with predefined options", lambda: st.select_slider("Select size", ["S", "M", "L", "XL"])),
    ("st.text_input", "Creates a single-line text input", lambda: st.text_input("Enter your name")),
    ("st.number_input", "Creates a numeric input", lambda: st.number_input("Enter a number", min_value=0, max_value=100, value=50)),
    ("st.text_area", "Creates a multi-line text input", lambda: st.text_area("Enter a paragraph")),
    ("st.date_input", "Creates a date input", lambda: st.date_input("Select a date")),
    ("st.time_input", "Creates a time input", lambda: st.time_input("Select a time")),
    ("st.file_uploader", "Creates a file uploader", lambda: st.file_uploader("Choose a file")),
    ("st.camera_input", "Creates a camera input widget", lambda: st.camera_input("Take a picture")),
    ("st.columns", "Creates a horizontal layout", lambda: st.columns(3)[1].write("This is in the middle column")),
    ("st.tabs", "Creates a tabbed interface", lambda: st.tabs(["Tab 1", "Tab 2", "Tab 3"])[1].write("This is Tab 2")),
    ("st.container", "Creates a container for elements", lambda: st.container().write("This is inside a container")),
    ("st.empty", "Creates an empty placeholder", lambda: st.empty().write("This replaces the empty placeholder")),
    ("st.form", "Creates a form for batch submission", lambda: st.form(key="my_form").form_submit_button("Submit")),
    ("st.plotly_chart", "Displays a Plotly chart", lambda: st.plotly_chart(px.scatter(x=[1, 2, 3], y=[1, 3, 2]))),
    ("st.pyplot", "Displays a Matplotlib figure", lambda: st.pyplot(plt.figure(figsize=(4,3))).add_subplot(111).plot([1, 2, 3])),
    ("st.bokeh_chart", "Displays a Bokeh chart", lambda: st.bokeh_chart(figure(plot_width=300, plot_height=300).circle([1, 2, 3], [1, 2, 3], size=20))),
    ("st.pydeck_chart", "Displays a PyDeck chart", lambda: st.pydeck_chart(pdk.Deck(initial_view_state=pdk.ViewState(latitude=37.76, longitude=-122.4, zoom=11)))),
    ("st.graphviz_chart", "Displays a Graphviz graph", lambda: st.graphviz_chart('''
        digraph {
            A -> B
            B -> C
            C -> A
        }
    ''')),
    ("st.balloons", "Displays a balloon animation", lambda: st.balloons()),
    ("st.snow", "Displays a snow animation", lambda: st.snow()),
    ("st.sidebar", "Adds elements to the sidebar", lambda: st.sidebar.write("This is in the sidebar")),
    ("st.markdown", "Renders Markdown text", lambda: st.markdown("**Bold** and *italic* text")),
]

def get_sidebar_style(sidebar_image_base64):
    return f"""
    <style>
    [data-testid="stSidebar"] {{
        background-image: url("data:image/png;base64,{sidebar_image_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Main game function
def run_game():
    st.title("🔍 Streamlit Scavenger Hunt!")
    st.subheader("Guess the Streamlit Element")

    sidebar_image_path = os.path.join(os.path.dirname(__file__), "images", "boy_and_dog.png")
    sidebar_image_base64 = get_base64_of_bin_file(sidebar_image_path)
    st.markdown(get_sidebar_style(sidebar_image_base64), unsafe_allow_html=True)

    if st.session_state.current_element is None:
        st.session_state.current_element = secrets.choice(elements)

    st.write("What Streamlit function creates this element?")

    # Display the element
    st.session_state.current_element[2]()

    # Get user's guess
    user_guess = st.text_input("Your guess (e.g., st.button):")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Submit"):
            check_answer(user_guess)

    with col2:
        if st.button("Skip"):
            st.session_state.current_element = secrets.choice(elements)
            st.rerun()

    # Display score and progress
    st.sidebar.markdown(f"""<h3 style='color: white;
                        margin-top: 150px;
                        '>Game Progress</h3>""", unsafe_allow_html=True)
                        
    st.sidebar.markdown(f"""<h4 style='color: white;
                        '>Score: {st.session_state.score}</h4>""", unsafe_allow_html=True)
                        
    st.sidebar.markdown(f"""<h4 style='color: white;
                        '>Questions Asked: {st.session_state.questions_asked}</h4>""", unsafe_allow_html=True)
    
    # Display a progress bar
    progress = st.session_state.questions_asked / 20  # Assuming 20 questions per game
    st.sidebar.progress(progress)

    if st.session_state.questions_asked >= 20:
        end_game()

def check_answer(user_guess):
    if user_guess.lower() == st.session_state.current_element[0]:
        st.success("Correct! 🎉")
        st.balloons()
        st.session_state.score += 1
    else:
        st.error(f"Not quite. It was {st.session_state.current_element[0]}")
        st.info(f"Description: {st.session_state.current_element[1]}")

    st.session_state.questions_asked += 1
    st.session_state.current_element = secrets.choice(elements)
    time.sleep(2)  # Give user time to see the result
    st.rerun()

def end_game():
    st.title("🏆 Game Over!")
    st.write(f"Your final score: {st.session_state.score} out of {st.session_state.questions_asked}")
    
    # Calculate percentage
    percentage = (st.session_state.score / st.session_state.questions_asked) * 100
    st.write(f"You got {percentage:.2f}% correct!")

    # Give a rating based on percentage
    if percentage >= 90:
        st.success("Outstanding! You're a Streamlit expert! 🌟")
    elif percentage >= 70:
        st.success("Great job! You're well on your way to mastering Streamlit! 😊")
    elif percentage >= 50:
        st.info("Good effort! Keep practicing and you'll improve! 👍")
    else:
        st.info("Nice try! Streamlit has a lot to offer. Keep exploring! 💪")

    if st.button("Play Again"):
        st.session_state.score = 0
        st.session_state.questions_asked = 0
        st.session_state.current_element = None
        st.rerun()

# Run the game
run_game()
