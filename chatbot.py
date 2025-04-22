import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

print("Starting chatbot")

def chat_with_grok():
    """Main function to run the chatbot"""
    print("\n=== GROK AI CHATBOT ===")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    
    # Initialize the Grok client with API key from .env
    grok_api_key = os.getenv("GROK_API_KEY")
    if not grok_api_key:
        print("Error: GROK_API_KEY not found in environment variables.")
        return
    
    print(f"Using Grok API key: {grok_api_key[:5]}...{grok_api_key[-5:]}")
    
    # API endpoint
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    
    # API headers
    headers = {
        "Authorization": f"Bearer {grok_api_key}",
        "Content-Type": "application/json"
    }
    
    # Keep track of conversation
    messages = []
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        try:
            # Add user message to conversation
            messages.append({"role": "user", "content": user_input})
            
            # Request payload
            payload = {
                "model": "llama3-8b-8192",  # Using Groq's LLama3 model
                "messages": messages,
                "temperature": 0.7
            }
            
            print("Sending request to Groq API...")
            # Call the Groq API
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Parse the response
            response_data = response.json()
            
            # Extract and display the response content
            if response_data and "choices" in response_data and len(response_data["choices"]) > 0:
                assistant_message = response_data["choices"][0]["message"]["content"]
                print(f"\nGrok: {assistant_message}\n")
                
                # Add assistant response to conversation history
                messages.append({"role": "assistant", "content": assistant_message})
            else:
                print("\nGrok: I'm having trouble generating a response. Please try again.\n")
                print(f"Response: {response_data}")
        except requests.exceptions.HTTPError as http_err:
            print(f"\nHTTP Error: {http_err}")
            print(f"Response content: {response.text if hasattr(response, 'text') else 'No response content'}")
        except Exception as e:
            print(f"\nError: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    chat_with_grok() 