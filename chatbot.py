
import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
Answer the following questions:
Here is the conversation hisotry: {context}
Question: {question}
Answer:
"""


model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def conversation_history():
    context = ""
    print ("Welcome to Pato's ChatBot! Type 'exit' to quit")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        result = chain.invoke({"context": context, "question": user_input})
        print("PatBot: ", result)
        context += f"\nuser: {user_input} \nAI: {result}"

if __name__ == "__main__":
    conversation_history()

