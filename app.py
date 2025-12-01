import streamlit as st
import requests
import json
import time
import os

model = "coderspace"  
ollama_url = "http://localhost:11434/api/chat"

def response_generator(msg_content):
    lines = msg_content.split('\n')
    for line in lines:
        words = line.split()
        for word in words:
            yield word + " "
            time.sleep(0.1)
        yield "\n"

def show_msgs():
    for msg in st.session_state.messages:
        role = msg["role"]
        with st.chat_message(role):
            st.write(msg["content"])

def chat(messages):
    try:
        response = requests.post(
            ollama_url,
            json={"model": model, "messages": messages, "stream": True},
        )
        response.raise_for_status()
        output = ""
        for line in response.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(body["error"])
            if body.get("done", False):
                return {"role": "assistant", "content": output}
            output += body.get("message", {}).get("content", "")
    except Exception as e:
        return {"role": "assistant", "content": str(e)}

def format_messages_for_summary(messages):
    # Create a single string from all the chat messages
    return '\n'.join(f"{msg['role']}: {msg['content']}" for msg in messages)


def summary(messages):
    sysmessage = "summarize this conversation in 3 words. No symbols or punctuation:\n\n\n"
    combined = sysmessage + messages
    api_message = [{"role": "user", "content": combined}]
    try:
        response = requests.post(
            ollama_url,
            json={"model": model, "messages": api_message, "stream": True},
        )
        response.raise_for_status()
        output = ""
        for line in response.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(body["error"])
            if body.get("done", False):
                return output
            # This will append only the content from each message, if available.
            output += body.get("message", {}).get("content", "")
    except Exception as e:
        return str(e)

def main():
    st.title("Code Assistant Chatbot with Streamlit and OLLAMA")
    user_input = st.chat_input("Enter your prompt:", key="1")
    if 'show' not in st.session_state:
        st.session_state['show'] = 'True'
    if 'show_chats' not in st.session_state:
        st.session_state['show_chats'] = 'False'
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    show_msgs()
    if user_input:
        with st.chat_message("user",):
                st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        combined = "\\n".join(msg["content"] for msg in st.session_state.messages if msg["role"] == "user")
        messages = [{"role": "user", "content": combined}]
        response = chat(messages)
        st.session_state.messages.append(response)
        with st.chat_message("assistant"):
                placeholder = st.empty()
                current_content = ""
                for chunk in response_generator(response["content"]):
                    current_content += chunk
                    placeholder.markdown(current_content)
    elif st.session_state['messages'] is None:
        st.info("Enter a prompt or load chat above to start the conversation")

if __name__ == "__main__":
    main()