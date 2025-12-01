# 📚 CoderSpace Chatbot

A **local AI code assistant** built using **Streamlit/Gradio** and **Ollama**, allowing users to interact with a LLM (Large Language Model) locally. The chatbot helps in generating code, explaining programming concepts, and answering coding questions in real-time. 

The project is structured for scalability, and maintainability.
---

## Requirements

- Python 3.10+
- Local Ollama server running the **Coderspace model**.
- GPU-enabled environment recommended for faster response.

## Features

- Chat with a local **Coderspace model** via Ollama API.
- Stream responses in real-time for better interactivity.
- Streamlit-based **responsive UI** with user-friendly design and custom icons for roles. 

## Technologies Used:
- Streamlit, Gradio, Python
- Models used: CoderSpace (custom model over **Codellama** model)

## Project Structure

```bash
coder_space_chatbot/
│
├─ app.py                # Main Streamlit application
├─ gradio_app.py         # Main Gradio application
├─ request.py            # Simple request check for ollama
├─ coderspace.modelfile  # modelfile to modify the codellama
└─ requirements.txt      # Python dependencies
```

## Installation

## 🛠 Installation (without Docker)

### 1. Clone the repo
```bash
git clone https://github.com/AmreetNanda/CodeAssistant_LLM.git
cd CodeAssistant_LLM
```
### 2. Requirements.txt
```bash
langchain
langchain_community
langchain-core
langchain-classic
gradio
ipykernel
streamlit
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. build the custom model
```bash
run in cmd -> ollama create coderspace -f coderspace.modelfile
           -> ollama run coderspace
```

### 5. Run Streamlit app
```bash
streamlit run app.py   # streamlit application
python gradio_app.py   # If want to run the app using Gradio

```
Open in your browser:
```
👉 http://localhost:8501/
👉 Enter the prompt in the text bex and hit enter.
👉 The model will then process the prompt entered and will generate the appropriate response accordingly.
```

## 🐳 Running with Docker (optional)
### Build the image
```bash
docker build -t coderspace-chatbot .
```

### Run the container
```bash
docker run -p 8501:8501 coderspace-chatbot
```
```
- Open: 👉 http://localhost:8501
- Note that the Ollama server is running locally as the chatbot communitcates with it for responses
- For GPU support inside docker use a CUDA enabled base image and run with "--gpus all"
docker run --gpus all -p 8501:8501 coderspace-chatbot

```

##### Home page
![App Screenshot](https://github.com/AmreetNanda/CodeAssistant_LLM/blob/main/CodeChatbot%20screenshot.png)


## Demo
https://github.com/user-attachments/assets/a006cdc9-e55b-4435-82b0-5d24d5d6c2d4

## License
[MIT](https://choosealicense.com/licenses/mit/)
## Screenshots
