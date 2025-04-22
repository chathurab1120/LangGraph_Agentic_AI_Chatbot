import os
import streamlit as st
from dotenv import load_dotenv
from enhanced_chatbot import create_agent, process_message

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Enhanced AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# App title and description
st.title("🤖 Enhanced AI Chatbot")
st.markdown("""
This chatbot uses LangGraph with REACT architecture to provide intelligent responses using multiple tools:
- 📚 Arxiv: For academic paper searches
- 📖 Wikipedia: For general knowledge queries
- 🔍 Tavily Search: For real-time internet searches
""")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None

# Check for API keys
api_key = os.getenv("GROK_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

# API key input in sidebar
with st.sidebar:
    st.subheader("API Configuration")
    if not api_key:
        api_key = st.text_input("Enter your Groq API Key:", type="password")
        if api_key:
            os.environ["GROK_API_KEY"] = api_key
    
    if not tavily_api_key:
        tavily_api_key = st.text_input("Enter your Tavily API Key:", type="password")
        if tavily_api_key:
            os.environ["TAVILY_API_KEY"] = tavily_api_key
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Initialize agent if needed
if not st.session_state.agent and api_key and tavily_api_key:
    with st.spinner("Initializing AI agent..."):
        st.session_state.agent = create_agent()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if st.session_state.agent:
    if prompt := st.chat_input("Ask me anything..."):
        # Display user message
        st.chat_message("user").markdown(prompt)
        
        # Process message with agent
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Process the message and update history
                new_messages = process_message(
                    st.session_state.agent,
                    prompt,
                    st.session_state.messages
                )
                
                # Update messages in session state
                st.session_state.messages = new_messages
                
                # Display new messages (excluding the last user message which we already showed)
                for msg in new_messages[len(st.session_state.messages):]:
                    if msg["role"] != "user":
                        st.markdown(msg["content"])
else:
    st.warning("Please provide both Groq and Tavily API keys in the sidebar to continue.")