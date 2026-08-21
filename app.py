import streamlit as st
from openai import OpenAI

st.title("My AI Chatbot")

# Get API key from Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):

    # Show user's message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Ask the LLM
    with st.chat_message("assistant"):
        response = client.responses.create(
            model="gpt-5-mini",
            input=st.session_state.messages
        )

        answer = response.output_text
        st.markdown(answer)

    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
