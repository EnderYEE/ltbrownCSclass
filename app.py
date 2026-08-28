import streamlit as st
from groq import Groq

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="My AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# ============================================================
# TITLE
# ============================================================

st.title("My AI Assistant")
st.write("Powered by Groq")

# ============================================================
# CHECK GROQ API KEY
# ============================================================

if "GROQ_API_KEY" not in st.secrets:
    st.error(
        "GROQ_API_KEY is missing. "
        "Please add your Groq API key to Streamlit Secrets."
    )
    st.stop()

# ============================================================
# CONNECT TO GROQ
# ============================================================

try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
except Exception as e:
    st.error(f"Could not connect to Groq: {e}")
    st.stop()

# ============================================================
# SIDEBAR
# ============================================================

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
            "You are a helpful, friendly, and knowledgeable AI "
            "assistant. Give clear and accurate answers. "
            "Explain difficult topics in a simple way."
        ),
        height=160
    )

    st.divider()

    if st.button(
        "Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

# ============================================================
# CHAT MEMORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================================
# USER INPUT
# ============================================================

prompt = st.chat_input(
    "Ask me anything..."
)

if prompt:

    # --------------------------------------------------------
    # Display user's message
    # --------------------------------------------------------

    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user's message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # --------------------------------------------------------
    # Prepare messages for Groq
    # --------------------------------------------------------

    messages_for_api = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages_for_api.extend(
        st.session_state.messages
    )

    # --------------------------------------------------------
    # Ask Groq
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        try:

            response = client.chat.completions.create(
                model=model,
                messages=messages_for_api,
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
                f"Groq returned an error:\n\n{e}"
            )
