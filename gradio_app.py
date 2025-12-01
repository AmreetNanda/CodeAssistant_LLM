# import requests
# import json
# import gradio as gr

# url = "http://localhost:11434/api/generate"

# headers = {'Content-Type':'application/json',}
# history =[]

# def generate_response(prompt):
#     history.append(prompt)
#     final_prompt = "\n".join(history)

#     data = {
#         "model": "coderspace",
#         "prompt": final_prompt,
#         "stream":False
#     }

#     response = requests.post(url, headers=headers, data= json.dumps(data))

#     if response.status_code == 200:
#         response = response.text
#         data = json.loads(response)
#         actual_response = data['response']
#         return actual_response
#     else:
#         print("Error:", response.text)

# interface = gr.Interface(fn=generate_response,
#                          inputs=gr.Textbox(lines=2, placeholder="Enter your prompt"),
#                          outputs="text")

# interface.launch()


import requests
import json
import gradio as gr

# --------------------
# OLLAMA API SETTINGS
# --------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
HEADERS = {"Content-Type": "application/json"}

# --------------------
# CHAT HISTORY
# --------------------
chat_history = []

# --------------------
# FUNCTION TO CALL OLLAMA
# --------------------
def generate_response(prompt):
    # Add user message to history
    chat_history.append(("user", prompt))

    # Build full prompt with context
    full_prompt = ""
    for role, text in chat_history:
        if role == "user":
            full_prompt += f"USER: {text}\n"
        else:
            full_prompt += f"ASSISTANT: {text}\n"
    full_prompt += f"USER: {prompt}\nASSISTANT:"

    # API request
    data = {
        "model": "coderspace",
        "prompt": full_prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        result = json.loads(response.text)
        bot_reply = result["response"]
        chat_history.append(("bot", bot_reply))
        return chat_history
    else:
        return [("bot", f"Error: {response.text}")]

# --------------------
# FUNCTION TO FORMAT CHAT
# --------------------
def format_chat(chat_history):
    formatted = ""
    for role, msg in chat_history:
        if role == "user":
            formatted += f"<div class='user-message'><b>🧑 You:</b> {msg}</div>"
        else:
            formatted += f"<div class='bot-message'><b>🤖 CoderSpace:</b> {msg}</div>"
    return formatted

# --------------------
# CUSTOM CSS
# --------------------
css = """
#chatbox {
    height: 500px;
    overflow-y: auto;
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #ddd;
    background-color: #f9f9f9;
}
.user-message {
    background-color: #DCF8C6;
    padding: 10px 14px;
    border-radius: 12px;
    margin-bottom: 10px;
    max-width: 75%;
}
.bot-message {
    background-color: #F1F0F0;
    padding: 10px 14px;
    border-radius: 12px;
    margin-bottom: 10px;
    max-width: 75%;
}
"""

import requests
import json
import gradio as gr

# Ollama API
OLLAMA_URL = "http://localhost:11434/api/generate"
HEADERS = {"Content-Type": "application/json"}
chat_history = []


# Generate response from Ollama
def generate_response(prompt):
    chat_history.append(("user", prompt))
    full_prompt = ""
    for role, msg in chat_history:
        full_prompt += f"{role.upper()}: {msg}\n"
    full_prompt += "ASSISTANT:"

    data = {
        "model": "coderspace",
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()
        bot_reply = json.loads(response.text)["response"]
        chat_history.append(("bot", bot_reply))
        return format_chat(chat_history)
    except Exception as e:
        chat_history.append(("bot", f"Error: {str(e)}"))
        return format_chat(chat_history)

def format_chat(chat_history):
    formatted = ""
    for role, msg in chat_history:
        # Preserve code blocks and spacing
        msg = msg.replace("\n", "<br>").replace("    ", "&nbsp;&nbsp;&nbsp;&nbsp;")
        if role == "user":
            formatted += f"""
            <div class='user-message' style='color:black; word-wrap: break-word;'>
                <b>🧑 You:</b> {msg}
            </div>
            """
        else:
            formatted += f"""
            <div class='bot-message' style='color:black; word-wrap: break-word;'>
                <b>🤖 CoderSpace:</b> {msg}
            </div>
            """
    return formatted



# --------------------
# CSS for polished UI
# --------------------
css = """
#chatbox {
    height: 550px;
    overflow-y: auto;
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #ddd;
    background-color: #f5f5f5;
    font-size: 16px;
    line-height: 1.5;
}
.user-message {
    background-color: #DCF8C6;
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 10px;
    max-width: 75%;
    font-size: 16px;
}
.bot-message {
    background-color: #FFFFFF;
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 10px;
    max-width: 75%;
    font-size: 16px;
    white-space: pre-wrap;
    font-family: monospace;
}
#submit-btn {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
}
#user-input {
    font-size: 16px;
}
"""

# --------------------
# Gradio UI
# --------------------
with gr.Blocks() as demo:
    gr.HTML(f"<style>{css}</style>")

    gr.Markdown("<h1 style='text-align:center;'>🤖 CoderSpace AI Assistant</h1>")
    gr.Markdown("<p style='text-align:center;'>Your local code-teaching assistant powered by Ollama + GPU</p>")

    chat_display = gr.HTML(elem_id="chatbox")
    user_input = gr.Textbox(
        label="Type your message here...",
        placeholder="Ask me anything about coding...",
        elem_id="user-input",
        lines=3
    )
    submit_btn = gr.Button("Send", elem_id="submit-btn")

    # Respond function
    def respond(prompt):
        return generate_response(prompt)

    submit_btn.click(respond, inputs=user_input, outputs=chat_display)
    submit_btn.click(lambda: "", None, user_input)

    # Clear chat button
    def clear_chat():
        chat_history.clear()
        return ""

    gr.Button("Clear Chat").click(clear_chat, outputs=chat_display)

# Launch
demo.launch()
