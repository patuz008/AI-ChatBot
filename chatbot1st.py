import streamlit as st
import ollama

# Configuration
MODEL = "llama3.2"  # Adjust to the actual available model name if needed
TEMPERATURE = 0.7
MAX_TOKENS = 100
SYSTEM_PROMPT = "You are an Expert."

# Initialize session state for messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def chat(user_input):
    """Handle chat interaction with the Ollama model."""
    # Append user input to messages
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call Ollama API
    response = ollama.chat(
        model=MODEL,
        messages=st.session_state.messages,
        options={
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS
        }
    )

    # Extract assistant's reply
    reply = response["message"]["content"]
    st.session_state.messages.append({"role": "assistant", "content": reply})
    
    return reply

# Streamlit UI
st.title("Pat AI ChatBot")
st.write("Type your message below and press Enter to chat. Type 'exit' or 'quit' to clear the conversation.")

# Input box for user message
user_input = st.text_input("Your message:", key="user_input")

# Handle user input
if user_input:
    if user_input.strip().lower() in {"exit", "quit"}:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.success("Conversation cleared! Start a new chat.")
    else:
        # Get assistant response
        with st.spinner("Thinking..."):
            response = chat(user_input)
        
        # Display the conversation
        for message in st.session_state.messages[1:]:  # Skip system prompt
            if message["role"] == "user":
                st.markdown(f"**You**: {message['content']}")
            else:
                st.markdown(f"**Assistant**: {message['content']}")

# Optional: Add a button to clear conversation
if st.button("Clear Conversation"):
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.success("Conversation cleared!")