---
title: Kaushik AI Digital Twin
app_file: app.py
sdk: gradio
sdk_version: 6.14.0
---

# AI Digital Twin — Kaushik Santhosh

A personal AI assistant that acts as a conversational representation of my professional profile. It uses my résumé/profile context together with Google's Gemini model to answer questions about my skills, education, projects, technical interests and experience.

## What this project demonstrates

- LLM/API integration using an OpenAI-compatible Gemini endpoint
- Context-grounded conversational AI
- Prompt engineering for a consistent professional persona
- Tool calling for optional lead capture and unknown-question logging
- Gradio-based interactive chatbot UI
- Environment-variable based secret management
- A reusable architecture that can be adapted to another person's profile

## Tech stack

**Python · Gradio · Gemini API · OpenAI Python SDK · PyPDF · python-dotenv · Requests**

## How it works

```text
Visitor
  ↓
Gradio Chat Interface
  ↓
System Prompt + Professional Context
  ↓
Gemini LLM
  ↓
Context-grounded Digital Twin Response
```

The application reads `summary.txt` and `linkedin.pdf`, builds a system prompt from that professional context, and sends the conversation to Gemini. The model is instructed not to invent achievements and to remain focused on career, education, skills and experience.

## Example questions

- Tell me about Kaushik.
- What are his strongest technical skills?
- What projects and experiences has he worked on?
- What is he learning about AI?
- Tell me about his education.
- How can I get in touch with him?

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

5. Start the app:

```bash
python app.py
```

## Configuration

`GOOGLE_API_KEY` is required. `PUSHOVER_USER` and `PUSHOVER_TOKEN` are optional and are only used for notification-based lead capture / unknown-question logging.

> Secrets are intentionally excluded from this repository. Never commit a real `.env` file or API key.

## Portfolio note

This public version uses my real professional profile as the knowledge source while excluding private credentials and unnecessary local-development files. The same architecture can be reused by replacing the profile context with another user's professional information.

## Live demo

A hosted Gradio demo can be connected here after deployment so recruiters can interact with the Digital Twin directly from a browser.
