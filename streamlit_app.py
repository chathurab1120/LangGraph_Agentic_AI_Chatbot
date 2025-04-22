import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Groq AI Chatbot",
    page_icon="💬",
    layout="centered"
)

# App title and description
st.title("💬 Groq AI Chatbot")
st.markdown("Chat with the Groq LLama3 model")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to call Groq API
def query_groq(messages, api_key):
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": messages,
        "temperature": 0.7
    }
    
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

# Get API key from environment or let user input it
api_key = os.getenv("GROK_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")
    if not api_key:
        st.warning("Please enter your Groq API key in the sidebar to continue.")
        st.stop()

# Chat input
if prompt := st.chat_input("Ask something..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant thinking
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # Call Groq API
            response = query_groq(st.session_state.messages, api_key)
            
            if response and "choices" in response and len(response["choices"]) > 0:
                assistant_response = response["choices"][0]["message"]["content"]
                
                # Update placeholder with assistant response
                message_placeholder.markdown(assistant_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            else:
                message_placeholder.markdown("I'm having trouble generating a response. Please try again.")
        except Exception as e:
            message_placeholder.markdown(f"Error: {str(e)}")

# Sidebar options
with st.sidebar:
    st.subheader("About")
    st.markdown("This is a chat interface powered by Groq's LLama3 model.")
    
    # Clear chat button
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()