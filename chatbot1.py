import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Template for the conversation
template = """
Answer the following questions:
Here is the conversation history: {context}
Question: {question}
Answer:
"""

# Initialize the chain components
@st.cache_resource
def initialize_chain():
    """Initialize the LLM and chain - cached to avoid recreation on every run"""
    model = OllamaLLM(model="llama3.2")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain

# Initialize the chain
try:
    chain = initialize_chain()
except Exception as e:
    st.error(f"Failed to initialize chatbot: {e}")
    st.stop()

# Streamlit UI
st.title("Pato's ChatBot")
st.markdown("Welcome to Pato's ChatBot! Ask me anything.")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "context" not in st.session_state:
    st.session_state.context = ""

# Display conversation history using proper chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get user input
if user_input := st.chat_input("Type your message here..."):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Invoke the chatbot chain
                result = chain.invoke({
                    "context": st.session_state.context, 
                    "question": user_input
                })
                
                # Display AI response
                st.write(result)
                
                # Add AI message to session state
                st.session_state.messages.append({"role": "assistant", "content": result})
                
                # Update context for future conversations
                st.session_state.context += f"\nuser: {user_input}\nAI: {result}"
                
            except Exception as e:
                st.error(f"Error generating response: {e}")

# Optional: Add a button to clear conversation
if st.button("Clear Conversation"):
    st.session_state.messages = []
    st.session_state.context = ""
    st.rerun()