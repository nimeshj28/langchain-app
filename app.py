import streamlit as st
import uuid
import json
from datetime import datetime
from database import init_database, save_session
from gemini_chat import TherapeuticChatbot
from analyzer import analyze_conversation
from image_generator import generate_motivational_image

# Initialize
init_database()

st.set_page_config(
    page_title="Life Journey Companion",
    page_icon="🌱",
    layout="wide"
)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.chatbot = None
    st.session_state.api_keys_set = False

if 'show_summary' not in st.session_state:
    st.session_state.show_summary = False

# Main App
st.title("🌱 Your Life Journey Companion")
st.subheader("A safe space to explore your thoughts and discover your strengths")

# API Keys Setup Section
if not st.session_state.get('api_keys_set', False):
    st.header("🔑 API Keys Setup")
    
    # API Key inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Required APIs")
        google_api_key = st.text_input(
            "🔵 Google Gemini API Key", 
            value="AIzaSyCG5BBFFpHfCU4oLYtAOU_D49q_9y3iJo0",
            type="password"
        )
        
        openai_api_key = st.text_input(
            "🟢 OpenAI API Key (Optional)", 
            value="",
            type="password"
        )
    
    with col2:
        st.subheader("Optional (for images)")
        hf_token = st.text_input(
            "🟡 HuggingFace Token", 
            value="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",
            type="password"
        )
    
    # Validation and setup
    if st.button("🚀 Start My Journey", type="primary"):
        if google_api_key:
            try:
                # Test Google API
                st.session_state.chatbot = TherapeuticChatbot(google_api_key)
                st.session_state.google_api_key = google_api_key
                st.session_state.openai_api_key = openai_api_key if openai_api_key else None
                st.session_state.hf_token = hf_token if hf_token else None
                st.session_state.api_keys_set = True
                
                st.success("✅ Setup complete! Let's begin your journey.")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error with Gemini API key: {str(e)}")
        else:
            st.error("❌ Google Gemini API key is required to start.")
    
    st.stop()

# Main Chat Interface
st.markdown("---")

# API Status indicators
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.success("🔵 Gemini: Connected")
with col2:
    if st.session_state.get('openai_api_key'):
        st.success("🟢 OpenAI: Connected")
    else:
        st.warning("🟢 OpenAI: Not set")
with col3:
    if st.session_state.get('hf_token'):
        st.success("🟡 HuggingFace: Connected")
    else:
        st.warning("🟡 HuggingFace: Not set")
with col4:
    if st.button("🔄 Reset API Keys"):
        for key in ['api_keys_set', 'google_api_key', 'openai_api_key', 'hf_token', 'chatbot']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

st.markdown("---")

# Chat Interface
chat_container = st.container()

with chat_container:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Initial message
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            initial_msg = "Hey! 👋 What would you like to talk about today? I'm here to listen and help you explore your thoughts."
            st.markdown(initial_msg)
            st.session_state.messages.append({"role": "assistant", "content": initial_msg})

# User input
if prompt := st.chat_input("Share what's on your mind..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chatbot.get_response(prompt, st.session_state.messages)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"❌ Gemini API Error: {str(e)}")
    
    # Save session after each exchange
    save_session(st.session_state.session_id, st.session_state.messages)

# "Done, please summarize" button
if len(st.session_state.messages) > 2:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Done, please summarize my session", use_container_width=True, type="primary"):
            st.session_state.show_summary = True

# Summary and Analysis Section
if st.session_state.show_summary:
    st.markdown("---")
    st.header("📊 Your Session Insights")
    
    with st.spinner("Analyzing your conversation..."):
        try:
            # Get analysis
            if st.session_state.get('openai_api_key'):
                analysis_result = analyze_conversation(
                    st.session_state.messages, 
                    st.session_state.get('openai_api_key')
                )
                analysis_data = json.loads(analysis_result)
            else:
                st.error("❌ OpenAI API key required for analysis")
                st.stop()
        except Exception as e:
            st.error(f"❌ OpenAI Analysis Error: {str(e)}")
            st.stop()
        
        # Display analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💭 Session Summary")
            st.write(analysis_data['summary'])
            
            st.subheader("😊 Emotions Detected")
            for emotion in analysis_data['emotions']:
                st.badge(emotion)
            
            st.subheader("💪 Your Strengths")
            for strength in analysis_data['strengths']:
                st.write(f"• {strength}")
        
        with col2:
            st.subheader("🌱 Growth Opportunities")
            for area in analysis_data['growth_areas']:
                st.write(f"• {area}")
            
            st.subheader("🎯 What You're Naturally Good At")
            st.info(analysis_data['natural_talent'])
            
            st.subheader("🚀 Unique Capabilities to Leverage")
            for capability in analysis_data['unique_capabilities']:
                st.write(f"• {capability}")
    
    # Generate motivational image
    st.subheader("🎨 Your Personalized Motivation")
    
    if st.session_state.get('hf_token'):
        with st.spinner("Creating your personalized image..."):
            try:
                image, image_prompt = generate_motivational_image(
                    analysis_data, 
                    st.session_state.get('hf_token')
                )
                st.image(image, caption="Your journey visualization", use_container_width=True)
                st.caption(f"Generated from: {image_prompt}")
            except Exception as e:
                st.error(f"❌ HuggingFace Image Error: {str(e)}")
    else:
        st.error("❌ HuggingFace token required for image generation")
    
    # Save complete session
    save_session(
        st.session_state.session_id, 
        st.session_state.messages,
        analysis_data['summary'],
        json.dumps(analysis_data),
        image_prompt if 'image_prompt' in locals() else "No image generated"
    )
    
    # Reset option
    if st.button("🔄 Start New Session"):
        keys_to_keep = ['google_api_key', 'openai_api_key', 'hf_token', 'api_keys_set']
        keys_backup = {k: st.session_state[k] for k in keys_to_keep if k in st.session_state}
        st.session_state.clear()
        st.session_state.update(keys_backup)
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.chatbot = TherapeuticChatbot(st.session_state.google_api_key)
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    🌱 <strong>Life Journey Companion</strong> - Your personal space for growth and self-discovery
</div>
""", unsafe_allow_html=True)