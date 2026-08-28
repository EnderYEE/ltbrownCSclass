import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="My AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("My AI Assistant")
st.write("Powered by Groq")

# Get Groq API key from Streamlit Secrets
if "GROQ_API_KEY" not in st.secrets:
    st.error(
        "GROQ_API_KEY is missing. "
        "Go to your Streamlit app settings and add your Groq API key "
        "under Secrets."
    )
    st.stop()

# Connect to Groq
try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
except Exception as e:
    st.error(f"Could not connect to Groq: {e}")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("Settings")

    model = st.selectbox(
        "AI Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ]
    )

    system_prompt = st.text_area(
        "AI Instructions",
        value=(
            "You are a helpful, friendly, and knowledgeable AI assistant. "
            "Give clear, accurate, and easy-to-understand answers."
        ),
        height=150
    )

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Create chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask me anything...")

if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Prepare messages for Groq
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages.extend(st.session_state.messages)

    # Get AI response
    with st.chat_message("assistant"):

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=2048
            )

            answer = response.choices[0].message.content

            st.markdown(answer)

            # Save AI response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:
            st.error(
                f"Groq returned an error: {e}"
            )
