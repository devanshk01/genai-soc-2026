# PromptForge

PromptForge is a small GenAI app where the same user prompt can be answered in different styles by changing the active persona.

The app currently supports 4 modes:

- Technical Explainer
- Debate Coach
- Code Reviewer
- Creative Writer

## What This App Does

- Lets the user switch between 4 personas with a dropdown
- Uses few-shot prompting so each persona has example behavior
- Streams responses token by token
- Shows the active system prompt in the UI
- Forces JSON output for Code Reviewer mode
- Parses Code Reviewer JSON and renders it as readable Markdown

## Project Files

- `app.py` - main Gradio app
- `requirements.txt` - minimal dependencies needed to run the app
- `.env.example` - sample environment file

## Run Locally

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in this folder and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

4. Start the app:

```bash
python app.py
```

5. Open the local Gradio URL in your browser.

## Mode Notes

### Technical Explainer

Best for simple, clear explanations without too much jargon.

### Debate Coach

Best for seeing both sides of a question in a balanced way.

### Code Reviewer

Best for structured code feedback. This mode asks the model for JSON, then renders:

- issues
- suggestions
- severity

If JSON parsing fails, the app shows a warning and the raw response.

### Creative Writer

Best for more descriptive, expressive, and narrative responses.

## Testing Notes

I checked the app logic for all 4 modes in code.

Things specifically handled:

- persona switching
- few-shot injection
- streaming response flow
- chat history normalization
- Code Reviewer JSON parsing with fallback

## Honest Limitations

- Code Reviewer mode depends on the model returning valid JSON. I added a fallback if parsing fails, but model output can still vary.
- This app currently focuses on prompt behavior and streaming. It is not a full production chat system.
