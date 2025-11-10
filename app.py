"""
AXIS AI - Streamlit Web Application
Advanced AI Assistant with Voice Recognition
"""

import streamlit as st
import os
import json
import time
from datetime import datetime
from dotenv import dotenv_values
from asyncio import run

# Backend imports
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech

# Try to import speech recognition - fallback to text input if not available
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

# Configuration
env_vars = dotenv_values(".env")
USERNAME = env_vars.get("Username", "User")
ASSISTANTNAME = env_vars.get("Assistantname", "Axis")
FUNCTIONS = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# Page configuration
st.set_page_config(
    page_title=f"{ASSISTANTNAME} AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1a2e 100%);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #1e3a5f;
        color: white;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #2d4a5f;
        color: white;
        margin-right: 20%;
    }
    .status-indicator {
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        display: inline-block;
        font-weight: bold;
    }
    .status-listening {
        background-color: #ff6b6b;
        color: white;
    }
    .status-thinking {
        background-color: #4ecdc4;
        color: white;
    }
    .status-answering {
        background-color: #95e1d3;
        color: #333;
    }
    .status-available {
        background-color: #a8e6cf;
        color: #333;
    }
    .mic-button {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
    }
    .mic-on {
        background-color: #ff6b6b;
    }
    .mic-off {
        background-color: #4ecdc4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'mic_status' not in st.session_state:
    st.session_state.mic_status = False
if 'assistant_status' not in st.session_state:
    st.session_state.assistant_status = "Available..."
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Cross-platform path helper
def get_data_dir():
    """Get the Data directory path, creating it if needed"""
    data_dir = os.path.join(os.getcwd(), 'Data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

# Load chat history from JSON
def load_chat_log():
    chatlog_path = os.path.join(get_data_dir(), 'ChatLog.json')
    if os.path.exists(chatlog_path):
        try:
            with open(chatlog_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Error loading chat log: {e}")
            return []
    return []

# Save chat history to JSON
def save_chat_log(messages):
    chatlog_path = os.path.join(get_data_dir(), 'ChatLog.json')
    try:
        with open(chatlog_path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving chat log: {e}")

# Initialize chat history
if not st.session_state.chat_history:
    chat_log = load_chat_log()
    if chat_log:
        st.session_state.chat_history = chat_log
    else:
        # Default welcome message
        welcome_msg = {
            "role": "assistant",
            "content": f"Welcome {USERNAME}! I am {ASSISTANTNAME}, your advanced AI assistant. How may I help you?"
        }
        st.session_state.chat_history = [welcome_msg]
        save_chat_log(st.session_state.chat_history)

# Helper functions
def AnswerModifier(answer):
    lines = answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def QueryModifier(query):
    new_query = query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", 
                      "can you", "what's", "where's", "how's"]
    
    if any(word + " " in new_query for word in question_words):
        if query_words and query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words and query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    
    return new_query.capitalize()

# Speech recognition function
def recognize_speech_from_audio(audio_file):
    """Convert audio to text using speech_recognition"""
    if not SPEECH_AVAILABLE:
        return None
    
    try:
        import tempfile
        import io
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
        
        r = sr.Recognizer()
        with sr.AudioFile(tmp_path) as source:
            audio = r.record(source)
        text = r.recognize_google(audio)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return QueryModifier(text)
    except Exception as e:
        st.error(f"Speech recognition error: {e}")
        return None

# Main execution function
def process_query(query):
    """Process user query through AI pipeline"""
    if not query or query.strip() == "":
        return None
    
    st.session_state.processing = True
    st.session_state.assistant_status = "Thinking..."
    
    # Add user message to chat
    st.session_state.chat_history.append({"role": "user", "content": query})
    save_chat_log(st.session_state.chat_history)
    
    try:
        # Get decision from DMM
        Decision = FirstLayerDMM(query)
        
        # Analyze decision types
        G = any([i for i in Decision if i.startswith("general")])
        R = any([i for i in Decision if i.startswith("realtime")])
        
        Merged_query = " and ".join(
            [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
        )
        
        TaskExecution = False
        ImageExecution = False
        ImageGenerationQuery = ""
        
        # Check for image generation
        for q in Decision:
            if "generate " in q:
                ImageGenerationQuery = str(q)
                ImageExecution = True
        
        # Check for automation tasks
        for q in Decision:
            if not TaskExecution:
                if any(q.startswith(func) for func in FUNCTIONS):
                    try:
                        run(Automation(list(Decision)))
                        TaskExecution = True
                    except Exception as e:
                        st.warning(f"Automation task failed: {e}")
        
        # Handle image generation
        if ImageExecution:
            st.info(f"🎨 Image generation requested: {ImageGenerationQuery}")
            # Note: Image generation would need to be handled separately in Streamlit
        
        # Handle realtime search
        if (G and R) or R:
            st.session_state.assistant_status = "Searching..."
            answer = RealtimeSearchEngine(QueryModifier(Merged_query))
            st.session_state.assistant_status = "Answering..."
            
            # Add assistant response
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            save_chat_log(st.session_state.chat_history)
            
            return answer
        
        # Handle general queries
        else:
            for q in Decision:
                if "general" in q:
                    st.session_state.assistant_status = "Thinking..."
                    QueryFinal = q.replace("general ", "")
                    answer = ChatBot(QueryModifier(QueryFinal))
                    st.session_state.assistant_status = "Answering..."
                    
                    # Add assistant response
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    save_chat_log(st.session_state.chat_history)
                    
                    return answer
                    
                elif "realtime" in q:
                    st.session_state.assistant_status = "Searching..."
                    QueryFinal = q.replace("realtime ", "")
                    answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                    st.session_state.assistant_status = "Answering..."
                    
                    # Add assistant response
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    save_chat_log(st.session_state.chat_history)
                    
                    return answer
                    
                elif "exit" in q:
                    answer = "Goodbye! Have a great day!"
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    save_chat_log(st.session_state.chat_history)
                    return answer
        
    except Exception as e:
        error_msg = f"I apologize, but I encountered an error: {str(e)}"
        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        save_chat_log(st.session_state.chat_history)
        return error_msg
    finally:
        st.session_state.processing = False
        st.session_state.assistant_status = "Available..."
    
    return None

# Main UI
def main():
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title(f"🤖 {ASSISTANTNAME} AI Assistant")
        st.caption(f"Welcome, {USERNAME}!")
    
    # Status bar
    status_emoji = {
        "Listening...": "🎤",
        "Thinking...": "🤔",
        "Answering...": "💬",
        "Searching...": "🔍",
        "Available...": "✅"
    }
    emoji = status_emoji.get(st.session_state.assistant_status, "✅")
    st.info(f"{emoji} **Status:** {st.session_state.assistant_status}")
    
    st.divider()
    
    # Chat display area with scrollable container
    st.markdown("### 💬 Chat History")
    chat_container = st.container(height=500)
    with chat_container:
        for idx, message in enumerate(st.session_state.chat_history):
            role = message.get("role", "assistant")
            content = message.get("content", "")
            
            if role == "user":
                with st.chat_message("user"):
                    st.write(f"**{USERNAME}:** {content}")
            else:
                with st.chat_message("assistant"):
                    st.write(f"**{ASSISTANTNAME}:** {content}")
    
    st.divider()
    
    # Input area
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Text input
        if 'user_input_text' in st.session_state:
            default_text = st.session_state.user_input_text
            del st.session_state.user_input_text
        else:
            default_text = ""
        
        user_input = st.text_input(
            "Type your message here...",
            value=default_text,
            key="user_input",
            disabled=st.session_state.processing
        )
        
        # Voice input section
        with st.expander("🎤 Voice Input (Alternative)"):
            if SPEECH_AVAILABLE:
                st.info("Upload an audio file (.wav format) for speech recognition")
                audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])
                if audio_file is not None:
                    with st.spinner("Processing audio..."):
                        recognized_text = recognize_speech_from_audio(audio_file)
                        if recognized_text:
                            st.success(f"Recognized: {recognized_text}")
                            if st.button("Use this text"):
                                user_input = recognized_text
                                st.session_state.user_input_text = recognized_text
            else:
                st.warning("Speech recognition not available. Install 'SpeechRecognition' package.")
        
        # Buttons
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        with col_btn1:
            send_button = st.button("📤 Send", type="primary", disabled=st.session_state.processing or not user_input)
            if send_button and user_input:
                process_query(user_input)
                st.rerun()
        
        with col_btn2:
            if st.button("🔄 Refresh", disabled=st.session_state.processing):
                st.rerun()
        
        with col_btn3:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                save_chat_log([])
                st.rerun()
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        st.subheader("Microphone Status")
        mic_status_text = "🟢 ON" if st.session_state.mic_status else "🔴 OFF"
        st.write(mic_status_text)
        
        st.subheader("Chat History")
        st.write(f"{len(st.session_state.chat_history)} messages")
        
        if st.button("📥 Export Chat"):
            chat_json = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button(
                label="Download Chat History",
                data=chat_json,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        st.divider()
        st.caption(f"Powered by Gemini AI & Cohere DMM")
        st.caption(f"Version 1.0.0")

if __name__ == "__main__":
    main()

