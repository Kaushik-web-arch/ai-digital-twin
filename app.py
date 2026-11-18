import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, OpenAI

from context import TWIN_SYSTEM_PROMPT
from styles import CSS, EXAMPLES, JS
from tools import handle_tool_calls, notifications_enabled, tools

load_dotenv(Path(__file__).with_name(".env"))

MODEL_NAME = os.getenv("GEMINI_MODEL", "").strip() or "gemini-3.1-flash-lite"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
MAX_TOOL_ROUNDS = 3

api_key = os.getenv("GOOGLE_API_KEY", "").strip()
client = (
    OpenAI(base_url=GEMINI_BASE_URL, api_key=api_key, timeout=30, max_retries=0)
    if api_key and api_key != "your_google_gemini_api_key_here"
    else None
)


def chat(message, history):
    if not client:
        raise gr.Error("Set GOOGLE_API_KEY in .env and restart the app.")
    if not message.strip():
        raise gr.Error("Enter a question to start chatting.")

    context = TWIN_SYSTEM_PROMPT
    options = {}
    if notifications_enabled():
        options["tools"] = tools
    else:
        context += "\nNotifications are disabled. If asked to forward a message, explain that forwarding is unavailable."

    messages = [{"role": "system", "content": context}]
    messages.extend(
        {"role": item["role"], "content": item["content"]}
        for item in history
        if item["role"] in {"user", "assistant"} and isinstance(item["content"], str)
    )
    messages.append({"role": "user", "content": message})

    try:
        for round_number in range(MAX_TOOL_ROUNDS + 1):
            response = client.chat.completions.create(
                model=MODEL_NAME, messages=messages, **options
            )
            if not response.choices:
                break
            reply = response.choices[0].message
            if not reply.tool_calls:
                if reply.content and reply.content.strip():
                    return reply.content
                break
            if not options or round_number == MAX_TOOL_ROUNDS:
                break
            messages.append(reply.model_dump(exclude_none=True))
            messages.extend(handle_tool_calls(reply.tool_calls))
    except APIConnectionError:
        raise gr.Error("Could not reach Gemini. Check your connection and try again.") from None
    except APIStatusError as error:
        detail = {
            401: "Check your Gemini API key.",
            403: "Check your Gemini API key and project permissions.",
            404: "Check that GEMINI_MODEL is available to your API key.",
            429: "Gemini's rate or quota limit was reached. Try again later.",
        }.get(error.status_code, "Gemini could not complete this request. Try again later.")
        raise gr.Error(detail) from None

    raise gr.Error("Gemini returned no usable answer. Try rephrasing your question.")


def build_demo():
    return gr.ChatInterface(
        fn=chat,
        examples=EXAMPLES,
        cache_examples=False,
        title="Kaushik Santhosh",
        description="AI Digital Twin · Software Development · Data Science · Artificial Intelligence",
        chatbot=gr.Chatbot(show_label=False, height=560),
    )


if __name__ == "__main__":
    build_demo().launch(
        server_name=os.getenv("HOST", "127.0.0.1"),
        server_port=int(os.getenv("PORT", "7860")),
        css=CSS,
        js=JS,
        theme=gr.themes.Base(),
        share=False,
    )
