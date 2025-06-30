import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Travel Buddy",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .error-message {
        background-color: #ffe6e6;
        color: #d63384;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #d63384;
    }
</style>
""", unsafe_allow_html=True)

class TravelBuddy:
    def __init__(self):
        self.client = None
        self.setup_client()
    
    def setup_client(self):
        """Initialize Groq client"""
        try:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                st.error(" GROQ_API_KEY not found in environment variables.")
                return False
            
            self.client = Groq(api_key=api_key)
            return True
        except Exception as e:
            st.error(f"Error initializing Groq client: {str(e)}")
            return False
    
    def get_response(self, message):
        """Get response from Groq API"""
        if not self.client:
            return " Client not initialized. Please check your API key configuration."
        
        try:
            system_message = """You are Travel Buddy, a friendly and knowledgeable travel assistant. Help users with:

• Tourist attractions and sightseeing
• Hotel and accommodation recommendations  
• Local food and restaurant suggestions
• Transportation and travel tips
• Budget planning and cost estimates
• Cultural insights and customs
• Itinerary planning

Be helpful, enthusiastic, and provide practical advice. Keep responses conversational and engaging."""

            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=800,
                top_p=1,
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Sorry, I'm having trouble connecting right now. Error: {str(e)}"

def main():
    # Header
    st.markdown('<h1 class="main-header"> Travel Buddy</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Your AI travel companion for planning amazing trips!</p>', unsafe_allow_html=True)
    
    # Initialize chatbot
    if 'travel_buddy' not in st.session_state:
        st.session_state.travel_buddy = TravelBuddy()
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant", 
                "content": " Hi there! I'm Travel Buddy, your personal travel assistant.\n\nWhat destination are you curious about today?"
            }
        ]
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant", avatar="🌍"):
                st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask me about travel destinations, hotels, food, or anything travel-related...")
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)
        
        # Get and display bot response
        with st.chat_message("assistant", avatar="🌍"):
            with st.spinner("Let me think about that..."):
                response = st.session_state.travel_buddy.get_response(user_input)
                st.write(response)
        
        # Add assistant response to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Sidebar with quick tips
    with st.sidebar:
        st.markdown("###  Quick Tips")
        st.markdown("""
        **Try asking about:**
        - "Best places to visit in Tokyo"
        - "Budget hotels in Paris"
        - "Local food in Thailand"
        - "3-day itinerary for Rome"
        - "Travel tips for India"
        """)
        
    #     st.markdown("---")
    #     st.markdown("### 🔧 Setup")
    #     st.markdown("Make sure your `.env` file contains:")
    #     st.code("GROQ_API_KEY=your_api_key_here")
        
        if st.button("Clear Chat History"):
            st.session_state.chat_history = [
                {
                    "role": "assistant", 
                    "content": "Hi there! I'm Travel Buddy, your personal travel assistant."
                }
            ]
            st.rerun()

if __name__ == "__main__":
    main()