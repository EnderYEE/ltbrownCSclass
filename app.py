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
st.caption("Powered by Groq")

# ============================================================
# GROQ API KEY
# ============================================================

if "GROQ_API_KEY" not in st.secrets:
    st.error(
        "GROQ_API_KEY is missing from Streamlit Secrets."
    )
    st.info(
        "Open your Streamlit app settings, go to Secrets, "
        "and add your Groq API key."
    )
    st.stop()

api_key = st.secrets["GROQ_API_KEY"]

# ============================================================
# CREATE GROQ CLIENT
# ============================================================

try:
    client = Groq(api_key=api_key)
except Exception as error:
    st.error("Could not connect to Groq.")
    st.code(str(error))
    st.stop()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Settings")

    # Current Groq production model
    model = st.selectbox(
        "Choose an AI model",
        [
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b"
        ]
    )

    system_prompt = st.text_area(
        "AI Instructions",
        value=(
            "You are a helpful, friendly, and knowledgeable "
            "AI assistant. Give clear and accurate answers. "
            "Explain difficult topics in simple language "
            "and use examples when helpful."
        ),
        height=180
    )

    st.divider()

    if st.button(
        "Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("AI Assistant")
    st.caption("Powered by Groq")

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
    # DISPLAY USER MESSAGE
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
    # PREPARE MESSAGE HISTORY
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
    # SEND REQUEST TO GROQ
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        try:

            response = client.chat.completions.create(
                model=model,
                messages=messages_for_api,
                temperature=0.7,
                max_completion_tokens=2048
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

        except Exception as error:

            st.error(
                "Groq returned an error."
            )

            st.code(str(error))
