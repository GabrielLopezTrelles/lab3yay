import streamlit as st
import google.generativeai as genai
    
st.set_page_config(page_title="Music Chatbot", page_icon="", layout="wide")

key = st.secrets["key"]

genai.configure(api_key = key)

st.title("Music Chatbot")
st.markdown("Ask me anything about music. Your question can be about artists, genres, history, recommendations, and more!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        system_instruction="""You are Music Chatbot, an expert AI assistant who knows 
        everything about music. You can discuss artists, albums, song history, genres, 
        music theory, concert experiences, music recommendations, and the music industry. 
        Keep your responses conversational, engaging, and informative. 
        Don't look up real-time data or streaming stats — focus on knowledge-based 
        music discussion."""
    )
    st.session_state.chat_session = model.start_chat(history=[])

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask me about music...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = st.session_state.chat_session.send_message(user_input)
        assistant_reply = response.text

    except Exception as e:
        error_message = str(e).lower()

        if "quota" in error_message or "rate" in error_message or "429" in error_message:
            assistant_reply = f"FULL ERROR: {e}"
        elif "safety" in error_message or "blocked" in error_message:
            assistant_reply = "Error. I can't respond to that topic. Try asking me something else about music!"
        else:
            assistant_reply = f"Error. Something went wrong. Please try again. (Error: {str(e)})"

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": assistant_reply
    })

if st.session_state.chat_history:
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="""You are Music Guru, an expert AI assistant who knows 
            everything about music. You can discuss artists, albums, song history, genres, 
            music theory, concert experiences, music recommendations, and the music industry. 
            Keep your responses conversational, engaging, and informative.
            You do NOT look up real-time data or streaming stats — focus on knowledge-based 
            music discussion."""
        )
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
