from groq import Groq
import os
from dotenv import load_dotenv
import gradio as gr

load_dotenv()
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

def chat_stream(msg, history):
    """ Gradio chat function """
    messages = [{"role" : "system", "content" : "You are a GenAI expert."}]
    
    # conversation history
    for human, bot in history:
        messages.append({"role" : "user", "content" : human})
        messages.append({"role" : "assistant", "content" : bot})
        
    messages.append({"role" : "user", "content" : msg})
    
    stream = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = messages,
        stream = True   # enables streaming
    )
    
    accumulated = ""
    
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        accumulated += delta
        yield accumulated   # Gradio re-renders on each yield
        
# one-line chat UI with built-in streaming
gr.ChatInterface(
    fn = chat_stream,
    title = "My first AI chat app"
).launch()