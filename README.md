# Enhanced AI Chatbot with REACT Architecture

This is an intelligent chatbot that uses LangGraph with REACT (Reasoning and Acting) architecture to provide comprehensive responses using multiple tools.

## 🔗 Live Demo
Try the chatbot here: [LangGraph Agentic AI Chatbot](https://langgraph-agentic-ai-chatbot-react.streamlit.app)

## Features

- 📚 **Arxiv Integration**: Search and retrieve academic papers
- 📖 **Wikipedia Integration**: Access general knowledge
- 🔍 **Tavily Search**: Real-time internet search capabilities
- 🤖 **REACT Architecture**: Smart reasoning before taking actions
- 🎯 **Multi-tool Orchestration**: Seamlessly combines information from multiple sources

## Prerequisites

- Python 3.8 or higher
- Groq API key (get it from [Groq Console](https://console.groq.com/))
- Tavily API key (get it from [Tavily](https://tavily.com/))

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/chathurab1120/LangGraph_Agentic_AI_Chatbot_REACT_Structure.git
   cd LangGraph_Agentic_AI_Chatbot_REACT_Structure
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Copy `.env.example` to `.env`
   - Add your API keys to the `.env` file:
     ```
     GROK_API_KEY=your_grok_api_key_here
     TAVILY_API_KEY=your_tavily_api_key_here
     ```

## Deployment

### Local Development
1. Start the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

2. If you haven't set the API keys in the `.env` file, you can enter them directly in the sidebar of the web interface

### Streamlit Cloud Deployment
1. Fork this repository to your GitHub account
2. Visit [Streamlit Cloud](https://share.streamlit.io/)
3. Create a new app and select this repository
4. In the Streamlit Cloud settings:
   - Set the Python version to 3.8 or higher
   - Add your API keys as secrets:
     ```toml
     GROK_API_KEY = "your_grok_api_key_here"
     TAVILY_API_KEY = "your_tavily_api_key_here"
     ```
5. Deploy!

## Usage Examples

You can ask the chatbot various types of questions, such as:

- "What are the latest papers on transformer architectures?"
- "Tell me about the history of quantum computing and recent developments"
- "What are the current applications of REACT architecture in AI systems?"

The chatbot will automatically:
1. Analyze your question
2. Choose the appropriate tool(s)
3. Gather information
4. Provide a comprehensive response

## Project Structure

- `streamlit_app.py`: Main Streamlit application
- `enhanced_chatbot.py`: Core chatbot logic with REACT architecture
- `requirements.txt`: Project dependencies
- `.env`: API key configuration
- `.streamlit/config.toml`: Streamlit theme configuration

## Security

- Never commit your API keys to the repository
- Use environment variables or Streamlit secrets for sensitive information
- The `.env` file is included in `.gitignore` to prevent accidental commits

## Contributing

Feel free to submit issues and enhancement requests!

## License

[MIT License](LICENSE) 