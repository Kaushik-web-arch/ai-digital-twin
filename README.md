# AI Digital Twin — Kaushik Santhosh

A personal AI assistant that acts as a conversational representation of my professional profile. It uses my résumé/profile context together with Google's Gemini model to answer questions about my skills, education, projects, technical interests and experience.

## What this project demonstrates

- LLM/API integration using Gemini
- Context-grounded conversational AI
- Prompt engineering for a consistent professional persona
- Tool calling for optional lead capture and unknown-question logging
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
2. Create and activate a Python virtual environment.
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
