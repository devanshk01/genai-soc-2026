from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key = os.getenv("GROQ_API_KEY"))

# Manually managing the conversation history as a global variable
conversation = [
    {
        "role" : "system",
        "content" : "You are a concise academic explainer. Keep every reponse under 100 words." 
    }
]

# Define a single chat
def chat (user_msg : str) -> str:
    # apoend the user msg to the convo.
    conversation.append({"role" : "user", "content" : user_msg})
    
    # get the response
    reponse = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = conversation,
        temperature = 0.7,
        max_tokens = 200
    )
    
    # get the reply from the reponse
    reply = reponse.choices[0].message.content
    # attach the reply to the convo.
    conversation.append({"role" : "assistant", "content" : reply})
    
    # return the reply
    return reply

# Keep asking for prompts until the program ends
# The model will remember the previous msgs
for _ in range(10):
    prompt = input("ENTER YOUR MSG HERE:\n")
    print('\n', chat(prompt), '\n', sep = '')
    
print("You have reached the limit of 10 messages!")