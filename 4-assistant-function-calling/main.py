import streamlit as st
import openai
from dotenv import load_dotenv
from assistant import call_assistant

load_dotenv()

client = openai.OpenAI()
MODEL_ENGINE = "gpt-3.5-turbo"

st.title("Chatbot - News & Weather Report")
st.subheader("Powered by OpenAI's GPT-3")
st.divider()
chat_placeholder = st.empty()


def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state.messages = [
            {"role": "system", "content": "You are a Finance Expert ."}
        ]


def start_chat():
    # Display chat messages from history on app rerun
    with chat_placeholder.container():
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            # Generate response from Chat models
            messages = call_assistant(prompt)
            filtered_msg = [message for message in messages if message.role != "user"]

            # message_placeholder.markdown(response)
            with st.chat_message("assistant"):
                for msg in filtered_msg:
                    message = msg.content[0].text.value
                    st.markdown(message)
                    # Add assistant's response to chat history
                    st.session_state.messages.append({"role": "assistant",
                                                      "content": message})


if __name__ == "__main__":
    init_chat_history()
    start_chat()
