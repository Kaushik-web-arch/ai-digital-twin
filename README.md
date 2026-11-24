# AI Digital Twin — Kaushik Santhosh

A personal AI assistant that acts as a conversational representation of my professional profile. It uses my résumé/profile context together with Google's Gemini model to answer questions about my skills, education, projects, technical interests and experience.

## What this project demonstrates

- LLM/API integration using Gemini
- Context-grounded conversational AI
- Prompt engineering for a consistent professional persona
- Optional unanswered-question notifications and a visitor-confirmed contact form
- Gradio-based interactive chatbot UI
- Environment-variable based secret management
- A reusable structure that can be adapted to another person's profile

## Tech stack

**Python · Gradio · Gemini API · OpenAI Python SDK · PyPDF · python-dotenv · Requests**

## How it works

```text
User
  ↓
Gradio Chat Interface
  ↓
System Prompt + Professional Context
  ↓
Gemini LLM
  ↓
Digital Twin Response
```

The application reads `summary.txt` and `linkedin.pdf`, builds a system prompt from that professional context, and uses Gemini to answer questions about my profile. The model is instructed to stay grounded in the supplied information and avoid inventing achievements.

## Example questions

- Tell me about Kaushik.
- What are his strongest technical skills?
- What projects and experiences has he worked on?
- What is he learning about AI?
- Tell me about his education.

## Run locally

1. Clone the repository.
2. Create and activate a Python 3.12 virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and add your Gemini API key:

```text
GOOGLE_API_KEY=your_key_here
```

5. Start the application:

```bash
python app.py
```

Open `http://127.0.0.1:7860`. The default model is `gemini-3.1-flash-lite`. Set `GEMINI_MODEL` in `.env` if your Gemini API key uses a different compatible model.

For a temporary public demo link, set `GRADIO_SHARE=true` in `.env` and restart `app.py`. Share the public URL printed in the terminal and keep the app running during the demo. On Windows PowerShell, run `.\.venv\Scripts\python.exe app.py` from the project folder.

## Project files

- `app.py` — main Gradio chatbot application
- `context.py` — builds the Digital Twin system prompt and loads profile context
- `tools.py` — optional tool-calling functions
- `styles.py` — UI styling and suggested questions
- `summary.txt` — professional summary used by the AI
- `linkedin.pdf` — professional profile context
- `requirements.txt` — Python dependencies

## Security

The real API key is not stored in this repository. Local credentials are kept in `.env`, which is ignored by Git.

## About this project

I built this project as a personal AI Digital Twin that can answer questions about my education, skills, projects and professional background. It also helped me explore practical LLM integration, prompt engineering, tool calling and conversational UI development.

## Implementation scope

[context.py](context.py) loads the PDF and summary directly into the system prompt. This is profile-grounded prompting: the current implementation has no embedding index, vector database, retrieval-ranking stage or fine-tuned model.

[app.py](app.py) passes conversation history to Gemini and executes requested functions through [tools.py](tools.py). This demonstrates function calling, not persistent cross-session memory.

### Optional notifications

Set `PUSHOVER_USER` and `PUSHOVER_TOKEN` in your local `.env` to enable a visitor-confirmed contact form and offer an unchecked option to forward unanswered questions. When credentials are absent, the chatbot runs without notification tools. The tools report whether Pushover accepted the request. Confirm receipt on the device to verify delivery. The app does not save contact or question records locally.

### Manual verification

1. Start the app and ask a question whose answer is present in the supplied profile.
2. Ask about an achievement absent from that profile and check that the answer acknowledges the missing information.
3. With your own test contact details and configured Pushover credentials, open Contact Kaushik, review the email and message, click Confirm and send, and independently confirm the notification arrives.
4. Record the commit, model, dependency versions and observed results without exposing credentials or personal contact details.

For four live review questions run `.\\.venv\\Scripts\\python.exe review_demo.py`. Open the resulting HTML file in a browser. Compare each answer with its expected facts before presenting. The saved transcript works offline. For a visual backup, record your running Gradio demo on the presentation laptop.

These are checks to perform, not recorded passing results. The repository currently has no automated test suite. Model access, notification delivery and factual quality require separate verification; no measured hallucination reduction is claimed.


### Local profile demo

On Windows PowerShell, set `$env:TWIN_LOCAL_MODE = "true"` before running `.\.venv\Scripts\python.exe app.py`. Local mode uses prepared profile answers. The chat also switches to local replies on temporary Gemini errors. Use the localhost address for an offline demo. The review script continues to check live Gemini replies.
