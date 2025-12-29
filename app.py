import streamlit as st
import uuid
from datetime import datetime
from config.settings import Settings
from aurion import GeminiEngine, PromptController, Memory, UserMemory, Assistant, VoiceHandler
from database import DatabaseHandler
from auth import (
    show_login_page,
    show_signup_page,
    show_profile_sidebar,
    check_authentication,
    initialize_auth_state
)


# Page configuration
st.set_page_config(
    page_title="JARVIS - AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        max-width: 900px;
    }
    
    .user-message {
        background-color: #E3F2FD;
        border-radius: 15px;
        padding: 12px 16px;
        margin: 8px 0;
        margin-left: 20%;
        border-left: 4px solid #2196F3;
    }
    
    .assistant-message {
        background-color: #F5F5F5;
        border-radius: 15px;
        padding: 12px 16px;
        margin: 8px 0;
        margin-right: 20%;
        border-left: 4px solid #4CAF50;
    }
    
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
    }
    
    .timestamp {
        font-size: 0.75rem;
        color: #888;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    # Initialize authentication
    initialize_auth_state()
    
    if 'settings' not in st.session_state:
        st.session_state.settings = Settings()
    
    if 'api_key' not in st.session_state:
        try:
            st.session_state.api_key = st.session_state.settings.load_api_key()
        except:
            st.session_state.api_key = None
    
    # Initialize database handler
    if 'db_handler' not in st.session_state:
        try:
            st.session_state.db_handler = DatabaseHandler()
        except Exception as e:
            st.error(f"Database connection failed: {e}")
            st.session_state.db_handler = None
    
    # Initialize memory based on authentication
    if 'memory' not in st.session_state:
        # Check if user is authenticated
        if check_authentication() and st.session_state.user:
            # Use UserMemory for authenticated users (database-backed)
            st.session_state.memory = UserMemory(
                user_id=st.session_state.user['user_id'],
                db_handler=st.session_state.db_handler
            )
        else:
            # Use regular Memory for non-authenticated (temp storage)
            st.session_state.memory = Memory()
    
    if 'assistant' not in st.session_state and st.session_state.api_key:
        engine = GeminiEngine(st.session_state.api_key)
        prompt_controller = PromptController()
        st.session_state.assistant = Assistant(
            engine, prompt_controller, st.session_state.memory
        )
    
    if 'current_conversation_id' not in st.session_state:
        st.session_state.current_conversation_id = None
    
    if 'assistant_role' not in st.session_state:
        st.session_state.assistant_role = "general"
    
    if 'streaming' not in st.session_state:
        st.session_state.streaming = True
    
    if 'voice_handler' not in st.session_state:
        st.session_state.voice_handler = VoiceHandler()
    
    if 'voice_input_text' not in st.session_state:
        st.session_state.voice_input_text = None


def create_new_conversation():
    """Create a new conversation"""
    conv_id = str(uuid.uuid4())[:8]
    st.session_state.memory.create_conversation(conv_id)
    st.session_state.current_conversation_id = conv_id
    return conv_id


def render_sidebar():
    """Render sidebar with conversation management"""
    with st.sidebar:
        st.markdown("### 🤖 JARVIS Assistant")
        
        # Show user profile
        show_profile_sidebar(st.session_state.db_handler)
        
        st.markdown("---")
        
        # New Conversation Button
        if st.button("➕ New Conversation", use_container_width=True):
            create_new_conversation()
            st.rerun()
        
        st.markdown("---")
        
        # Conversation List
        st.markdown("### 💬 Conversations")
        
        conversation_ids = st.session_state.memory.get_conversation_ids()
        
        if not conversation_ids:
            st.info("No conversations yet. Start a new one!")
        else:
            for conv_id in conversation_ids:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    is_current = conv_id == st.session_state.current_conversation_id
                    if st.button(
                        f"📝 Chat {conv_id[:4]}", 
                        key=f"select_{conv_id}",
                        use_container_width=True,
                        type="primary" if is_current else "secondary"
                    ):
                        st.session_state.memory.set_current_conversation(conv_id)
                        st.session_state.current_conversation_id = conv_id
                        st.rerun()
                
                with col2:
                    if st.button("🗑️", key=f"delete_{conv_id}"):
                        st.session_state.memory.delete_conversation(conv_id)
                        if st.session_state.current_conversation_id == conv_id:
                            st.session_state.current_conversation_id = None
                        st.rerun()
        
        st.markdown("---")
        
        # Settings
        st.markdown("### ⚙️ Settings")
        
        # Role Selection
        role = st.selectbox(
            "Assistant Mode",
            options=list(PromptController.get_available_roles().keys()),
            format_func=lambda x: PromptController.get_available_roles()[x],
            index=list(PromptController.get_available_roles().keys()).index(
                st.session_state.assistant_role
            )
        )
        
        if role != st.session_state.assistant_role:
            st.session_state.assistant_role = role
            if 'assistant' in st.session_state:
                st.session_state.assistant.set_role(role)
        
        # Streaming Toggle
        st.session_state.streaming = st.checkbox(
            "⚡ Stream Responses", 
            value=st.session_state.streaming
        )
        
        st.markdown("---")
        
        # Clear Current Conversation
        if st.session_state.current_conversation_id:
            if st.button("🧹 Clear Conversation", use_container_width=True):
                st.session_state.assistant.clear_memory(
                    st.session_state.current_conversation_id
                )
                st.success("Conversation cleared!")
                st.rerun()


def render_message(role, message, timestamp=None):
    """Render a single message"""
    if role == "user":
        st.markdown(f"""
        <div class="user-message">
            <strong>You</strong>
            <p>{message}</p>
            {f'<div class="timestamp">{timestamp}</div>' if timestamp else ''}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <strong>JARVIS</strong>
            <p>{message}</p>
            {f'<div class="timestamp">{timestamp}</div>' if timestamp else ''}
        </div>
        """, unsafe_allow_html=True)


def render_chat_interface():
    """Render main chat interface"""
    # Header
    st.markdown("""
    <div class="chat-header">
        <h1>🤖 JARVIS AI Assistant</h1>
        <p>Your intelligent personal assistant powered by Gemini</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current conversation
    if st.session_state.current_conversation_id is None:
        create_new_conversation()
    
    # Display chat history
    history = st.session_state.memory.get_history(
        st.session_state.current_conversation_id
    )
    
    if not history:
        st.markdown(f"""
        <div style="text-align: center; padding: 40px; color: #666;">
            <h3>👋 {st.session_state.assistant.get_greeting()}</h3>
            <p>Type a message or use voice input to start the conversation.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in history:
            try:
                dt = datetime.fromisoformat(msg['timestamp'])
                time_str = dt.strftime("%I:%M %p")
            except:
                time_str = None
            
            render_message(msg['role'], msg['message'], time_str)
    
    # Chat input area
    st.markdown("---")
    
    # Create two columns for text input and voice button
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.chat_input("Type your message here...")
    
    with col2:
        voice_button = st.button("🎤", use_container_width=True, help="Click to use voice input")
    
    # Handle voice input
    if voice_button:
        with st.spinner("🎤 Listening... Please speak now..."):
            recognized_text = st.session_state.voice_handler.recognize_speech_from_mic()
            
            if recognized_text:
                st.session_state.voice_input_text = recognized_text
                st.success(f"✅ Recognized: {recognized_text}")
                # Set a flag to process this input
                user_input = recognized_text
            else:
                st.error("❌ Could not understand the audio. Please try again.")
                st.info("💡 Tip: Speak clearly and ensure your microphone is working.")
    
    # Handle user input (from text or voice)
    if user_input:
        # Display user message
        render_message("user", user_input, datetime.now().strftime("%I:%M %p"))
        
        # Generate response
        with st.spinner("JARVIS is thinking..."):
            if st.session_state.streaming:
                # Streaming response
                response_placeholder = st.empty()
                full_response = ""
                
                for chunk in st.session_state.assistant.respond_stream(
                    user_input, 
                    st.session_state.current_conversation_id
                ):
                    full_response += chunk
                    response_placeholder.markdown(f"""
                    <div class="assistant-message">
                        <strong>JARVIS</strong>
                        <p>{full_response}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Regular response
                response = st.session_state.assistant.respond(
                    user_input, 
                    st.session_state.current_conversation_id
                )
                render_message("assistant", response, datetime.now().strftime("%I:%M %p"))
        
        # Clear voice input text after processing
        st.session_state.voice_input_text = None
        st.rerun()


def main():
    """Main application"""
    initialize_session_state()
    
    # Check authentication
    if not check_authentication():
        # Show login or signup page
        if st.session_state.get('show_signup', False):
            show_signup_page(st.session_state.db_handler)
        else:
            show_login_page(st.session_state.db_handler)
        return
    
    # User is authenticated - ensure memory and assistant are initialized with user data
    if st.session_state.user and st.session_state.db_handler:
        # Check if memory needs to be reinitialized for the logged-in user
        if not isinstance(st.session_state.memory, UserMemory):
            # Reinitialize with UserMemory for this user
            st.session_state.memory = UserMemory(
                user_id=st.session_state.user['user_id'],
                db_handler=st.session_state.db_handler
            )
            
            # Reinitialize assistant with new memory
            if st.session_state.api_key:
                engine = GeminiEngine(st.session_state.api_key)
                prompt_controller = PromptController(st.session_state.assistant_role)
                st.session_state.assistant = Assistant(
                    engine, prompt_controller, st.session_state.memory
                )
    
    # Check for API key (only for authenticated users)
    if not st.session_state.api_key:
        st.error("⚠️ Gemini API Key not found!")
        st.markdown("""
        Please set your Gemini API key in the `.env` file:
        """)
        return
    
    # Render UI for authenticated users
    render_sidebar()
    render_chat_interface()


if __name__ == "__main__":
    main()