# Groq AI Chatbot

A simple and efficient chatbot powered by Groq's LLama3 model.

## Features

- 💬 Simple chat interface
- 🤖 Powered by Groq's LLama3 model
- 🔒 Secure API key management
- 📱 Responsive Streamlit UI

## Prerequisites

- Python 3.8 or higher
- Groq API key (get it from [Groq Console](https://console.groq.com))

## Installation

1. Clone this repository:
```bash
git clone https://github.com/chathurab1120/LangGraph_Agentic_AI_Chatbot.git
cd LangGraph_Agentic_AI_Chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Copy `.env.example` to `.env`
   - Add your Groq API key to the `.env` file:
   ```
   GROK_API_KEY=your_grok_api_key_here
   ```

## Usage

1. Start the Streamlit app:
```bash
streamlit run streamlit_app.py
```

2. Open your browser and go to:
```
http://localhost:8501
```

3. If you haven't set the API key in the `.env` file, you can enter it directly in the sidebar of the web interface.

## Project Structure

- `streamlit_app.py`: Main Streamlit application
- `chatbot.py`: Core chatbot logic
- `requirements.txt`: Project dependencies
- `.env`: API key configuration
- `.streamlit/config.toml`: Streamlit theme configuration

## Security

- Never commit your API keys to the repository
- Use environment variables or Streamlit secrets for sensitive information
- The `.env` file is included in `.gitignore` to prevent accidental commits

## License

MIT License 