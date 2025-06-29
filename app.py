import streamlit as st
import http.client
import json

# --- ChatGPT-42 API Configuration ---
RAPIDAPI_HOST = "chatgpt-42.p.rapidapi.com"
RAPIDAPI_KEY = st.secrets["RAPIDAPI_KEY"]

# Define available API Endpoints
# Note: The behavior and response format might differ between these endpoints.
# The current parsing logic is tailored for the "/gpt4o" endpoint's "result" key.
# You might need to adjust the `get_chatgpt_response` function if other
# endpoints return data in a significantly different format.
API_ENDPOINTS = {
    "ChatGPT-4o (Default)": "/gpt4o",
    "Chat (General)": "/chat",
    "Deepseek AI": "/deepseekai",
    "GPT-4": "/gpt4",
    "O3 Mini": "/o3mini",
    "Conversational Llama 3": "/conversationallama3",
    "Matag Vision": "/matagvision",
    "ChatGPT (General)": "/chatgpt",
    "Matag 2": "/matag2",
    "Conversational GPT-4": "/conversationgpt4",
    "Conversational GPT-4-2": "/conversationgpt4-2",
}

# --- Streamlit App Setup ---
st.set_page_config(page_title="Erie - My Kinda ChatBot", page_icon="🤖")
st.title("🤖 Erie - My Kinda ChatBot")
st.markdown(
    """
    This chatbot connects to various AI models via the ChatGPT-42 RapidAPI.
    Select an endpoint from the sidebar and start chatting!
    """
)

# Initialize chat history in session state if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to clear chat history
def clear_chat_history():
    """Clears the messages in the session state."""
    st.session_state.messages = []
    # Re-run the app to clear displayed messages
    st.rerun()

# --- Sidebar for Controls ---
with st.sidebar:
    st.header("Settings")

    # Endpoint selection
    selected_endpoint_name = st.selectbox(
        "Choose an API Endpoint:",
        options=list(API_ENDPOINTS.keys()),
        index=0, # Default to ChatGPT-4o
        key="api_endpoint_selector"
    )
    # Store the actual endpoint path in session state
    st.session_state.current_api_endpoint = API_ENDPOINTS[selected_endpoint_name]

    # Clear chat button
    if st.button("Clear Chat", on_click=clear_chat_history):
        pass # Button click handled by on_click, no need for further action here

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to get response from the selected API endpoint
def get_chatgpt_response(user_message):
    """
    Sends a message to the selected API endpoint and returns the AI's response.
    The entire chat history is sent with each request to maintain context.
    """
    # Use the endpoint selected by the user
    current_endpoint = st.session_state.current_api_endpoint

    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)

    # Construct the payload by including the entire conversation history
    messages_payload = []
    for msg in st.session_state.messages:
        messages_payload.append({"role": msg["role"], "content": msg["content"]})
    # Append the current user message to the history for the API call
    messages_payload.append({"role": "user", "content": user_message})

    # The payload also includes 'web_access: false' as per the API's requirements
    payload = json.dumps({
        "messages": messages_payload,
        "web_access": False
    })

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST,
        'Content-Type': "application/json"
    }

    try:
        conn.request("POST", current_endpoint, payload, headers) # Use selected endpoint
        res = conn.getresponse()
        data = res.read()
        raw_response_str = data.decode("utf-8")

        try:
            response_data = json.loads(raw_response_str)
        except json.JSONDecodeError:
            st.error(f"Error: The API returned an unreadable response from {current_endpoint}. Please try again.")
            return "Sorry, I couldn't understand the API's response."

        # --- Extract the content from the API response based on its structure ---
        # The API is expected to return the main response in the 'result' key.
        # However, different endpoints might have different response formats.
        # This part might need further refinement based on actual responses from other endpoints.
        if response_data and response_data.get("result"):
            return response_data["result"]
        elif response_data and response_data.get("choices"): # Fallback for OpenAI-like structures
            if response_data["choices"][0].get("message") and response_data["choices"][0]["message"].get("content"):
                return response_data["choices"][0]["message"]["content"]
            else:
                st.error(f"Error: API response from {current_endpoint} was incomplete (missing message content). Raw: {raw_response_str}")
                return "Sorry, the API response was incomplete."
        else:
            # If neither 'result' nor 'choices' are found, the response format is unexpected
            st.error(f"Error: Unexpected API response format from {current_endpoint}. Raw: {raw_response_str}")
            return "Sorry, I couldn't get a valid response due to an unexpected API format."
    except http.client.HTTPException as http_err:
        st.error(f"HTTP Error from {current_endpoint}: {http_err}. Check your internet connection or API host/endpoint.")
        return "An HTTP error occurred. Please check your connection or API configuration."
    except Exception as e:
        st.error(f"An unexpected error occurred during API call to {current_endpoint}: {e}")
        return f"An unexpected error occurred: {e}. Please check your internet connection or API key."
    finally:
        conn.close()

# Accept user input in the chat input box
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history in session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message immediately in the chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response and display it
    with st.chat_message("assistant"):
        with st.spinner(f"Talking to {selected_endpoint_name}..."): # Show spinner with endpoint name
            assistant_response = get_chatgpt_response(prompt)
            st.markdown(assistant_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
