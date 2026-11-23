import ollama

response = ollama.chat(
    model="llama3.2:1b",
    messages=[
        {
            "role": "user",
            "content": "Explain what a Business Intelligence Agent does in simple words."
        }
    ]
)

print(response["message"]["content"])