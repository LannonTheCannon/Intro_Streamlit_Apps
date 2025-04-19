import streamlit as st
import secrets

st.title("Guess the Streamlit Element!")

elements = [
    ("st.button", "A clickable button"),
    ("st.slider", "A slidable control"),
    ("st.text_input", "A box for text entry"),
    ("st.selectbox", "A dropdown menu"),
    ("st.checkbox", "A toggleable option"),
    ("st.radio", "A set of circular options"),
    ("st.progress", "A progress bar"),
    ("st.balloons", "A celebration animation")
]

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'current_element' not in st.session_state:
    st.session_state.current_element = secrets.choice(elements)

st.write("What Streamlit function creates this element?")

# Display the element
if st.session_state.current_element[0] == "st.button":
    st.button("Click me!")
elif st.session_state.current_element[0] == "st.slider":
    st.slider("Slide me!", 0, 100)
elif st.session_state.current_element[0] == "st.text_input":
    st.text_input("Type here")
elif st.session_state.current_element[0] == "st.selectbox":
    st.selectbox("Choose an option", ["Option 1", "Option 2", "Option 3"])
elif st.session_state.current_element[0] == "st.checkbox":
    st.checkbox("Check me!")
elif st.session_state.current_element[0] == "st.radio":
    st.radio("Select one", ["A", "B", "C"])
elif st.session_state.current_element[0] == "st.progress":
    st.progress(0.5)
elif st.session_state.current_element[0] == "st.balloons":
    st.balloons()

# Get user's guess
user_guess = st.text_input("Your guess:")

if st.button("Submit"):
    if user_guess.lower() == st.session_state.current_element[0]:
        st.success("Correct! 🎉")
        st.session_state.score += 1
    else:
        st.error(f"Not quite. It was {st.session_state.current_element[0]}")

    st.session_state.current_element = secrets.choice(elements)
    st.rerun()

st.write(f"Current Score: {st.session_state.score}")
