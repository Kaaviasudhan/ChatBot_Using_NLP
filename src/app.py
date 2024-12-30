# src/app.py
import streamlit as st
from datetime import datetime
from nlp.infer import generate_response
from utils.file_handler import ConversationHandler
from utils.news_api import NewsAPI
from utils.faq_api import FAQAPI
from visualization.charts import plot_confidence_scores, plot_sentiment_analysis

# Initialize APIs and handlers
news_api = NewsAPI()
faq_api = FAQAPI()
conv_handler = ConversationHandler()

# Streamlit configuration
st.set_page_config(page_title="Enhanced NLP Chatbot", layout="wide")

# Session state initialization
if 'current_history_file' not in st.session_state:
    st.session_state.current_history_file = conv_handler.get_filename()
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar Menu
menu = st.sidebar.selectbox("Choose an option", 
                           ["Chat with Bot", "Chat History", "Analytics"])

# News Section in Sidebar
st.sidebar.markdown("### Latest News")
news_items = news_api.get_news(max_results=3)
for item in news_items:
    st.sidebar.markdown(f"**{item['title']}**")
    st.sidebar.markdown(item['description'])
    st.sidebar.markdown(f"[Read more]({item['url']})")
    st.sidebar.markdown("---")

if menu == "Chat with Bot":
    st.title("Chat with Your Bot")
    
    # Create columns for chat and real-time analytics
    chat_col, analytics_col = st.columns([2, 1])
    
    with chat_col:
        # Display current conversation
        for message in st.session_state.history:
            st.markdown(f"**You:** {message['user']}")
            st.markdown(f"**Bot:** {message['bot']}")
            if 'confidence' in message:
                st.progress(message['confidence'])
            st.markdown("---")
        
        # User input
        user_input = st.text_input("Type your message:", key="user_input")
        
        if st.button("Send"):
            if user_input:
                # Get response and confidence
                response, confidence = generate_response(user_input)
                
                # Get a random fact for variety
                fact = faq_api.get_fact()
                if fact and confidence < 0.5:  # Use fact if confidence is low
                    response = f"{response}\n\nHere's an interesting fact: {fact}"
                
                # Update history
                st.session_state.history.append({
                    "user": user_input,
                    "bot": response,
                    "confidence": confidence,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                # Save conversation
                conv_handler.save_conversation(
                    st.session_state.history,
                    st.session_state.current_history_file
                )
                
                # Clear input by refreshing the page
                st.rerun()
    
    with analytics_col:
        st.markdown("### Real-time Analytics")
        if st.session_state.history:  # Only show analytics if there are messages
            plot_confidence_scores(st.session_state.history)
            plot_sentiment_analysis(st.session_state.history)

elif menu == "Chat History":
    st.title("Chat History")
    
    # Get all history files
    histories = conv_handler.get_all_histories()
    
    if not histories:
        st.info("No chat history available yet.")
    else:
        # Display each history session
        for history in histories:
            with st.expander(f"Chat Session: {history['timestamp']}"):
                for message in history['messages']:
                    st.markdown(f"**You:** {message['user']}")
                    st.markdown(f"**Bot:** {message['bot']}")
                    if 'confidence' in message:
                        st.progress(message['confidence'])
                    st.markdown("---")

elif menu == "Analytics":
    st.title("Chat Analytics")
    
    # Load all histories for analysis
    all_histories = conv_handler.get_all_histories()
    
    if not all_histories:
        st.info("No chat history available for analysis.")
    else:
        # Combine all messages for analysis
        all_messages = []
        for history in all_histories:
            all_messages.extend(history['messages'])
        
        # Display analytics
        plot_confidence_scores(all_messages)
        plot_sentiment_analysis(all_messages)