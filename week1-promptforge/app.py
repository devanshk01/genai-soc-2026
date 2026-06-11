from groq import Groq
import os
import json
from dotenv import load_dotenv
import gradio as gr

load_dotenv()
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

# Technical Explainer Role
techFewShot = [
    {
        "role": "user",
        "content": "What is an API?"
    },
    {
        "role": "assistant",
        "content": "An API is a set of rules that lets two software programs talk to each other. It works like a menu in a restaurant: you choose what you want, and the system gives you the result without exposing how it is made."
    },
    {
        "role": "user",
        "content": "What is recursion?"
    },
    {
        "role": "assistant",
        "content": "Recursion is when a function solves a problem by calling itself on a smaller version of the same problem. It stops when it reaches a base case, which prevents it from calling itself forever."
    }
]

techExplainer = {
    "system_prompt" : "You are a concise, clear and jargon-free Technical Explainer.",
    "few_shot_examples" : techFewShot,
    "output_format" : "text"
}


# Debate Coach Role
debFewShot = [
    {
        "role": "user",
        "content": "Should students use AI tools for homework?"
    },
    {
        "role": "assistant",
        "content": "Argument for: AI tools can help students understand concepts faster, check their work, and get unstuck. Argument against: if used too much, they can reduce original thinking and make learning less effective. Balanced view: AI is useful when it supports learning, but students should still do the thinking themselves."
    },
    {
        "role": "user",
        "content": "Is remote work better than office work?"
    },
    {
        "role": "assistant",
        "content": "For remote work: it saves commute time, offers flexibility, and can improve focus. For office work: it makes collaboration easier, separates work from home, and can support faster communication. Overall: the better choice depends on the team, the job, and the person's working style."
    }
]

debCoach = {
    "system_prompt" : "You are a Debate Coach, who argues both sides of any question with balanced and structured arguments.",
    "few_shot_examples" : debFewShot,
    "output_format" : "text"
}


# Code Reviewer Role
codeFewShot = [
    {
        "role": "user",
        "content": "Review this code: `def add(a, b): return a + b`"
    },
    {
        "role": "assistant",
        "content": "{\n  \"issues\": [],\n  \"suggestions\": [\"Add a short docstring if this function is part of a larger codebase.\"],\n  \"severity\": \"low\"\n}"
    },
    {
        "role": "user",
        "content": "Review this code: `for i in range(len(items)): print(items[i])`"
    },
    {
        "role": "assistant",
        "content": "{\n  \"issues\": [\"Uses index-based iteration when direct iteration would be simpler.\"],\n  \"suggestions\": [\"Use `for item in items:` to make the code cleaner and easier to read.\"],\n  \"severity\": \"low\"\n}"
    }
]

codeReview = {
    "system_prompt" : "You are a precise Code Reviewer with strict JSON output formatter, detecting issues, providing suggestions and rating the severity.",
    "few_shot_examples" : codeFewShot,
    "output_format" : "json"
}


# Creative Writer Role
wriFewShot = [
    {
        "role": "user",
        "content": "Write a short opening line for a story set in a storm."
    },
    {
        "role": "assistant",
        "content": "The sky cracked open above the town, and the rain fell like a million silver needles stitching the night shut."
    },
    {
        "role": "user",
        "content": "Describe a lonely lighthouse."
    },
    {
        "role": "assistant",
        "content": "The lighthouse stood alone on the cliff, a pale tower wrapped in wind and salt, watching the sea with a patient, unwavering glow."
    }
]

creativeWriter = {
    "system_prompt" : "You are a Creative Writer with other worldly imagination, expressive tone and vivid language.",
    "few_shot_examples" : wriFewShot,
    "output_format" : "text"
}


# AI personas are managed here
personas = {
    "Technical Explainer" : techExplainer,
    "Debate Coach" : debCoach,
    "Code Reviewer" : codeReview,
    "Creative Writer" : creativeWriter 
}

# System prompt builder: adds extra JSON instructions for Code Reviewer mode
def buildSystemPrompt(persona):
    systemPrompt = persona["system_prompt"]
    
    if persona["output_format"] == "json":
        systemPrompt += " Return only valid JSON with these keys: issues, suggestions, severity. Do not add markdown, code fences or extra explanation."
    
    return systemPrompt

# History normalizer: converts Gradio chat history into role/content messages
def normalizeHistory(history):
    normalizedHistory = []
    
    if not history:
        return normalizedHistory
    
    for msg in history:
        if isinstance(msg, dict):
            normalizedHistory.append({
                "role" : msg["role"],
                "content" : msg["content"]
            })
        elif isinstance(msg, (list, tuple)) and len(msg) == 2:
            userText, assistantText = msg
            normalizedHistory.append({
                "role" : "user",
                "content" : userText
            })
            normalizedHistory.append({
                "role" : "assistant",
                "content" : assistantText
            })
        else:
            role = getattr(msg, "role", None)
            content = getattr(msg, "content", None)
            
            if role is not None and content is not None:
                normalizedHistory.append({
                    "role" : role,
                    "content" : content
                })
    
    return normalizedHistory

# Few-shot injector: adds the system prompt, examples, history and current user message
def fewShotInjector(persona, user_msg, history):
    conversation = []
    
    # Add the system prompt
    conversation.append({
        "role" : "system",
        "content" : buildSystemPrompt(persona)
    })
    
    # Add the few-shot examples
    fewShots = persona["few_shot_examples"]
    
    for fewShot in fewShots:
        conversation.append(fewShot.copy())
    
    # Add the chat history
    for msg in normalizeHistory(history):
        conversation.append(msg.copy())
        
    # Add the user msg
    conversation.append({
        "role" : "user",
        "content" : user_msg
    })
    
    return conversation

def formatList(items):
    if isinstance(items, list):
        if not items:
            return "- None"
        
        return "\n".join(f"- {item}" for item in items)
    
    if not items:
        return "- None"
    
    return f"- {items}"

def formatCodeReview(reviewData):
    issues = formatList(reviewData.get("issues", []))
    suggestions = formatList(reviewData.get("suggestions", []))
    severity = reviewData.get("severity", "unknown")
    
    return f"""### Code Review

**Severity:** {severity}

**Issues**
{issues}

**Suggestions**
{suggestions}"""

def parseCodeReview(rawText):
    cleanedText = rawText.strip()
    
    if cleanedText.startswith("```json"):
        cleanedText = cleanedText[7:]
    elif cleanedText.startswith("```"):
        cleanedText = cleanedText[3:]
    
    if cleanedText.endswith("```"):
        cleanedText = cleanedText[:-3]
    
    cleanedText = cleanedText.strip()
    
    try:
        return formatCodeReview(json.loads(cleanedText))
    except json.JSONDecodeError:
        return f"Warning: Could not parse JSON response.\n\n```json\n{rawText}\n```"

def generator(user_msg, history, persona_name, temperature):
    history = normalizeHistory(history)
    persona = personas[persona_name]
    conversation = fewShotInjector(persona = persona, user_msg = user_msg, history = history)
    
    stream = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = conversation,
        temperature = temperature,
        stream = True    
    )
    
    chatHistory = history + [{
        "role" : "user",
        "content" : user_msg
    }]
    full_text = ""
    
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        
        if not delta:
            continue
        
        full_text += delta
        yield chatHistory + [{
            "role" : "assistant",
            "content" : full_text
        }]
    
    if persona["output_format"] == "json":
        yield chatHistory + [{
            "role" : "assistant",
            "content" : parseCodeReview(full_text)
        }]

def promptViewer(persona_name):
    return buildSystemPrompt(personas[persona_name])

def clearInput():
    return ""
    
# Gradio chat app (Blocks UI)
with gr.Blocks(title = "PromptForge") as app:
    gr.Markdown("# PromptForge")
    
    # Mode selection and model settings
    with gr.Row():
        modeDropdown = gr.Dropdown(
            choices = list(personas.keys()),
            value = "Technical Explainer",
            label = "Mode"
        )
        
        tempSlider = gr.Slider(
            minimum = 0.0,
            maximum = 1.5,
            value = 0.7,
            step = 0.1,
            label = "Temperature"
        )
    
    # Active system prompt
    with gr.Accordion("Active System Prompt", open = False):
        systemPromptBox = gr.Textbox(
            value = personas["Technical Explainer"]["system_prompt"],
            label = "System Prompt",
            lines = 4,
            interactive = False
        )
    
    # Chat components
    chatbot = gr.Chatbot(label = "Conversation")
    userInput = gr.Textbox(label = "Your Message", placeholder = "Ask something here...")
    
    modeDropdown.change(
        fn = promptViewer,
        inputs = modeDropdown,
        outputs = systemPromptBox
    )
    
    userInput.submit(
        fn = generator,
        inputs = [userInput, chatbot, modeDropdown, tempSlider],
        outputs = chatbot
    ).then(
        fn = clearInput,
        outputs = userInput
    )

app.launch()
