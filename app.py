import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="My AI Chatbot")

st.title("🤖 My AI Chatbot")
st.write("Ask me anything!")

# Connect to OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Remember conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User enters a message
prompt = st.chat_input("Type your message...")

if prompt:
    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        try:
            response = client.responses.create(
                model="gpt-5.6-luna",
                input=st.session_state.messages
            )

            answer = response.output_text
            st.write(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(f"Error: {e}")
