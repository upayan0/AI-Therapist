# frontend.py
import streamlit as st
import requests

# -------------------------
# Config
# -------------------------
BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="🧠 SafeSpace – AI Therapist", layout="wide")

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.title("SafeSpace")
    st.markdown("""
    Welcome to **SafeSpace**, your AI mental health companion.
    
    - Chat about your feelings
    - Get empathetic guidance
    - Find local therapists
    - Immediate support for crisis situations
    """)
    st.markdown("---")
    st.markdown("**Tips for using this AI:**")
    st.markdown("""
    - Be honest about your feelings  
    - Use short messages for best responses  
    - Casual greetings are fine (“Hi”, “Hello”)  
    - For serious concerns, the system can escalate
    """)

# -------------------------
# Chat Interface
# -------------------------
st.title("🧠 SafeSpace Chat")
st.markdown("Talk to the AI mental health assistant below:")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Optional mood selector
mood = st.selectbox(
    "How are you feeling today?", 
    ["🙂 Good", "😐 Neutral", "😔 Sad", "😟 Anxious", "😢 Stressed"], 
    index=1
)

# Chat input
user_input = st.text_input("Type your message here...", key="user_input")

if st.button("Send") and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Backend call
    try:
        response = requests.post(BACKEND_URL, json={"message": user_input})
        data = response.json()
        reply_text = data.get("response", "Sorry, no response.")

        # Append assistant response (no agent/tool names)
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": reply_text
        })
    except Exception:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Error: could not reach backend."
        })

# -------------------------
# Display Chat with dark theme
# -------------------------
chat_container = st.container()

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        chat_container.markdown(
            f"<div style='text-align: right; background-color:#1E3A8A; color:white; padding:12px; border-radius:12px; margin:6px 0;'>"
            f"{msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        chat_container.markdown(
            f"<div style='text-align: left; background-color:#222222; color:white; padding:12px; border-radius:12px; margin:6px 0;'>"
            f"{msg['content']}</div>",
            unsafe_allow_html=True
        )

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.markdown("💡 *SafeSpace is an AI tool for supportive conversation and guidance, not a replacement for professional therapy.*")