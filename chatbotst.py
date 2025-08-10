

import ollama

MODEL = "llama3.2"  # adjust to the actual available model name if needed
TEMPERATURE = 0.7
MAX_TOKENS = 100
SYSTEM_PROMPT = "You are an Expert."

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def chat(user_input):

    messages.append({"role": "user", "content": user_input})

    response = ollama.chat(
        model=MODEL,
        messages=messages
    )
    # The Ollama API returns a dict, get the text content:
    reply = response["message"]["content"]
    messages.append({"role": "assistant", "content": reply})


    return reply

while True:
    user_input = input("User: ")
    if user_input.strip().lower() in {"exit", "quit"}:
        break
    answer = chat(user_input)
    print("User:", user_input)
    print("Assistant:", answer)

# print(chat("Hello! What's up?"))
