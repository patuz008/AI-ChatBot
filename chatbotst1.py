import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# ----- Prompt Template -----
template = """
Answer the following questions:
Here is the conversation history: {context}
Question: {question}
Answer:
"""

# Load model and prompt
model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# ----- Streamlit UI -----
st.set_page_config(page_title="Pato's ChatBot", page_icon="🤖", layout="centered")
st.title("🤖 Pato's ChatBot")
st.markdown("Chat with **LLaMA 3.2 (Ollama)** + LangChain")

# Session state for chat memory
if "context" not in st.session_state:
    st.session_state.context = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input at the bottom
user_input = st.chat_input("Type your message here...")

if user_input:
    # Generate bot response
    result = chain.invoke({"context": st.session_state.context, "question": user_input})

    # Save messages
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("PatoBot", result))

    # Update context for future
    st.session_state.context += f"\nYou: {user_input}\nAI: {result}"

# Display all messages
for role, message in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**PatoBot:** {message}")
