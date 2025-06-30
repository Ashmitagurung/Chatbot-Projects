from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from groq import Groq

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_groq_response(question, chat_history):
    """
    Function to get response from Groq API
    """
    try:
        # Prepare messages for the chat
        messages = []
        
        # Add chat history to messages
        for role, content in chat_history:
            if role == "You":
                messages.append({"role": "user", "content": content})
            else:
                messages.append({"role": "assistant", "content": content})
        
        # Add current question
        messages.append({"role": "user", "content": question})
        
        # Get response from Groq
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",  # You can change this to other available models
            temperature=0.7,
            max_tokens=1024,
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo with Groq")

st.header("Groq LLM Application")
st.subheader("Powered by Llama 3")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input field
user_input = st.text_input("Input: ", key="input", placeholder="Ask me anything...")
submit = st.button("Ask the question")

# Handle form submission
if submit and user_input:
    with st.spinner("Thinking..."):
        # Get response from Groq
        response = get_groq_response(user_input, st.session_state['chat_history'])
        
        # Add user query and response to session chat history
        st.session_state['chat_history'].append(("You", user_input))
        st.session_state['chat_history'].append(("Bot", response))
    
    # Clear the input field after submission
    st.rerun()

# Display current response if there's chat history
if st.session_state['chat_history']:
    st.subheader(" Chat History")
    
    # Display chat history in reverse order (most recent first)
    for i in range(len(st.session_state['chat_history']) - 1, -1, -2):
        if i > 0:  # Make sure we have both user and bot messages
            user_msg = st.session_state['chat_history'][i-1]
            bot_msg = st.session_state['chat_history'][i]
            
            # User message
            st.write("** You:**")
            st.write(user_msg[1])
            
            # Bot response
            st.write("**🤖 Bot:**")
            st.write(bot_msg[1])
            st.divider()

# Add a button to clear chat history
if st.session_state['chat_history']:
    if st.button("🗑️ Clear Chat History"):
        st.session_state['chat_history'] = []
        st.rerun()

# Sidebar with information
with st.sidebar:
    st.title("About")
    st.write("This chatbot uses Groq's API with Llama 3 model.")
    st.write("Enter your question and get AI-powered responses!")
    
    # st.subheader(" Configuration")
    # st.write("Model: llama3-8b-8192")
    # st.write("Temperature: 0.7")
    # st.write("Max Tokens: 1024")