```python
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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        .main {
            max-width: 900px;
            margin: auto;
        }

        .stChatMessage {
            border-radius: 12px;
        }

        h1 {
            text-align: center;
        }

        .subtitle {
            text-align: center;
            color: #777;
            margin-bottom: 30px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# TITLE
# ============================================================

st.title("My AI Assistant")
st.markdown(
    '<p class="subtitle">Powered by Groq</p>',
    unsafe_allow_html=True
)

# ============================================================
# CHECK API KEY
# ============================================================

if "GROQ_API_KEY" not in st.secrets:
    st.error(
        "Groq API key not found. Add GROQ_API_KEY to your "
        "Streamlit Secrets."
    )
    st.stop()

# ============================================================
# CREATE GROQ CLIENT
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

    # Model selection
    model = st.selectbox(
        "Choose AI model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ]
    )

    # AI personality
    system_prompt = st.text_area(
        "AI instructions",
        value=(
            "You are a helpful, friendly, and knowledgeable AI "
            "assistant. Give clear and accurate answers. "
            "Explain difficult topics in a simple way when "
            "appropriate."
        ),
        height=180
    )

    st.divider()

    # Clear conversation
    if st.button(
        "Clear conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("AI Assistant")
    st.caption("Built with Streamlit + Groq")

# ============================================================
# CHAT MEMORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================
# DISPLAY PREVIOUS MESSAGES
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
    # Display user message
    # --------------------------------------------------------

    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
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
    # Get AI response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        try:

            response = client.chat.completions.create(
                model=model,
                messages=messages_for_api,
                temperature=0.7,
                max_tokens=2048
            )

            answer = response.choices[0].message.content

            message_placeholder.markdown(answer)

            # Save AI response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:

            error_message = (
                "Sorry, something went wrong while contacting "
                f"the AI.\n\nError: `{e}`"
            )

            message_placeholder.error(
                error_message
            )
```
