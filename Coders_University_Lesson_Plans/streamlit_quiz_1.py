import streamlit as st
import secrets

# Quiz questions and answers
quiz_data = [
    {
        "question": "What is the primary purpose of Streamlit's Session State?",
        "answer": "To share variables between reruns of the app",
        "options": [
            "To share variables between reruns of the app",
            "To store global variables",
            "To cache function results",
            "To save data to a database"
        ]
    },
    {
        "question": "How do you initialize a variable in Session State?",
        "answer": "st.session_state.variable_name = value",
        "options": [
            "st.session_state.variable_name = value",
            "st.session_state['variable_name'] = value",
            "st.set_state(variable_name, value)",
            "st.init_state(variable_name, value)"
        ]
    },
    {
        "question": "What happens if you try to access a key that doesn't exist in Session State?",
        "answer": "It raises a KeyError",
        "options": [
            "It raises a KeyError",
            "It returns None",
            "It creates the key with a default value",
            "It throws a StreamlitAPIException"
        ]
    },
    {
        "question": "Can you store complex data structures like lists or dictionaries in Session State?",
        "answer": "Yes",
        "options": ["Yes", "No", "Only lists", "Only dictionaries"]
    },
    {
        "question": "How do you check if a key exists in Session State?",
        "answer": "if 'key_name' in st.session_state:",
        "options": [
            "if 'key_name' in st.session_state:",
            "if st.session_state.has_key('key_name'):",
            "if st.session_state.exists('key_name'):",
            "if 'key_name' in st.state:"
        ]
    },
    {
        "question": "What's the benefit of using Session State over global variables?",
        "answer": "It's specific to each user session and doesn't affect other users",
        "options": [
            "It's specific to each user session and doesn't affect other users",
            "It's faster than global variables",
            "It allows for larger data storage",
            "It automatically saves data to a database"
        ]
    },
    {
        "question": "How can you delete a variable from Session State?",
        "answer": "del st.session_state.variable_name",
        "options": [
            "del st.session_state.variable_name",
            "st.session_state.remove(variable_name)",
            "st.session_state.delete(variable_name)",
            "st.remove_state(variable_name)"
        ]
    },
    {
        "question": "Does Session State persist after the browser is closed?",
        "answer": "No, it's cleared when the session ends",
        "options": [
            "No, it's cleared when the session ends",
            "Yes, it's stored in the browser's local storage",
            "Yes, it's stored on the server",
            "It depends on the Streamlit configuration"
        ]
    },
    {
        "question": "Can you use Session State with Streamlit's callback functions?",
        "answer": "Yes",
        "options": ["Yes", "No", "Only with button callbacks", "Only with form submissions"]
    },
    {
        "question": "What's a common use case for Session State in Streamlit apps?",
        "answer": "Maintaining user input across app reruns",
        "options": [
            "Maintaining user input across app reruns",
            "Storing large datasets",
            "Managing database connections",
            "Caching API responses"
        ]
    }
]


def main():
    st.title("Streamlit Session State Quiz")

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.quiz_finished = False
        secrets.SystemRandom().shuffle(quiz_data)

    if not st.session_state.quiz_finished:
        question = quiz_data[st.session_state.current_question]
        st.write(f"Question {st.session_state.current_question + 1} of {len(quiz_data)}")
        st.write(question["question"])

        user_answer = st.radio("Choose your answer:", question["options"], key=f"q_{st.session_state.current_question}")

        if st.button("Submit Answer"):
            if user_answer == question["answer"]:
                st.success("Correct!")
                st.session_state.score += 1
            else:
                st.error(f"Wrong. The correct answer is: {question['answer']}")

            st.session_state.current_question += 1

            if st.session_state.current_question >= len(quiz_data):
                st.session_state.quiz_finished = True
            else:
                st.experimental_rerun()

    if st.session_state.quiz_finished:
        st.write(f"Quiz finished! Your score: {st.session_state.score}/{len(quiz_data)}")
        if st.button("Restart Quiz"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()


if __name__ == "__main__":
    main()
