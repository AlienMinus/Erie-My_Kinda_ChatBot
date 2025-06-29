# Erie - My Kinda ChatBot 🤖

This is a Streamlit-based chatbot app that connects to various AI models via the ChatGPT-42 RapidAPI. You can select different endpoints from the sidebar and chat with multiple AI models in a conversational interface.

## Features

- Multiple AI endpoints (ChatGPT-4o, GPT-4, Deepseek AI, Llama 3, and more)
- Maintains chat history per session
- Easily clear chat history
- Simple, interactive UI with Streamlit

## Setup

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd ChatBot
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.streamlit/secrets.toml` file in the project root (already present in this repo):

```toml
RAPIDAPI_KEY = "your_actual_rapidapi_key_here"
```

Replace the value with your [RapidAPI](https://rapidapi.com/) key for the ChatGPT-42 API.

### 4. Run the app

```sh
streamlit run app.py
```

## Usage

- Select an API endpoint from the sidebar.
- Type your message in the chat input box.
- View responses from the selected AI model.
- Use the "Clear Chat" button to reset the conversation.

## File Structure

- [`app.py`](app.py): Main Streamlit application.
- [`requirements.txt`](requirements.txt): Python dependencies.
- [`.streamlit/secrets.toml`](.streamlit/secrets.toml): API key storage (do not share your key publicly).

## Notes

- For production, always keep your API keys secure and never expose them in public repositories.
- The app is designed for demonstration and educational purposes.

---

Made with ❤️ using [Streamlit](https://streamlit.io/)