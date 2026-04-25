import streamlit as st
import google.generativeai as genai
import requests
baseUrl = "http://ws.audioscrobbler.com/2.0"
apiKey = "a28edaddcd62a1f9f8ae8100299fbc3b"

def musicData():
    try:
        UrlforArtist = baseUrl + "/?method=chart.gettopartists&api_key=" + apiKey + "&format=json"
        response = requests.get(UrlforArtist)
        data = response.json()
        return data
    except Exception as e:
        st.error(f"Error fetching music data: {e}")
        return None
    
def findRelevantArtists(data, query):
    try:
        artists = data["artists"]["artist"]
        results = []
        query_words = query.lower().split()

        for artist in artists:
            name = artist["name"].lower()

            if any(word in name for word in query_words):
                results.append(artist)
            
            if len(results) >= 5:
                break
        
        if not results:
            results = artists[:5]

        return results
    
    except Exception as e:
        st.error(f"Error finding relevant artists: {e}")
        return []
    
def formatArtists(artists):
    if not artists:
        return "No artists found."
    
    formatted = []
    for a in artists:
        name = a.get("name", "Unknown Artist")
        url = a.get("url", "No website")
        formatted.append(f"{name} - Website: {url}")
    return "\n".join(formatted)

st.set_page_config(page_title="Music Chatbot", page_icon="", layout="wide")

key = st.secrets["key"]

genai.configure(api_key = key)

st.title("Music Chatbot")
st.markdown("Ask me anything about music. Your question can be about artists, genres, history, recommendations, and more!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "api_data" not in st.session_state:
    st.session_state.api_data = musicData()

if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction="""You are Music Chatbot, an expert AI assistant who knows 
        everything about music. You can discuss artists, albums, song history, genres, 
        music theory, concert experiences, music recommendations, and the music industry. 
        Keep your responses conversational, engaging, and informative. 
        You are a music chatbot that uses provided external API data about artists to answer questions."""
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
        relevant = find_relevant_artists(st.session_state.api_data, user_input)
        api_context = format_artists(relevant)

        full_prompt = f"""
        You are a music chatbot. Use this external data when relevant:

        {api_context}

        User question: {user_input}
        Provide a helpful and informative answer based on the user's question and the provided artist data.
        """

        response = st.session_state.chat_session.send_message(full_prompt)
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
            You use provided external data to answer questions."""
        )
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()