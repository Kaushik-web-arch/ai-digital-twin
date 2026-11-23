import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, OpenAI

from context import TWIN_SYSTEM_PROMPT
from styles import CONTACT_PROMPT, CSS, EXAMPLES, JS, PROJECT_GROUPS
from tools import send_contact, handle_tool_calls, notifications_enabled, tools

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


def chat(message, history, allow_forwarding=False):
    if not client:
        raise gr.Error("Set GOOGLE_API_KEY in .env and restart the app.")
    if not message.strip():
        raise gr.Error("Enter a question to start chatting.")

    context = TWIN_SYSTEM_PROMPT
    options = {}
    if notifications_enabled():
        if allow_forwarding is True:
            options["tools"] = tools
        context += "\nFor contact requests, direct visitors to the Contact Kaushik form below the chat."
    else:
        context += "\nNotifications are disabled. If asked to forward a message, explain that forwarding is unavailable."

    messages = [{"role": "system", "content": context}]
    for item in history:
        if item.get("role") not in {"user", "assistant"}:
            continue
        content = item.get("content")
        if isinstance(content, list):
            content = "\n".join(
                part["text"] for part in content
                if isinstance(part, dict) and part.get("type") == "text"
                and isinstance(part.get("text"), str)
            )
        if isinstance(content, str) and content.strip():
            messages.append({"role": item["role"], "content": content})
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
    with gr.Blocks(title="Kaushik Santhosh | Digital Twin") as demo:
        gr.Markdown(
            "# Kaushik Santhosh\nAI Digital Twin · Projects, skills and experience",
            elem_id="twin-header",
        )
        with gr.Row(elem_id="twin-layout"):
            with gr.Column(scale=3, elem_id="twin-chat-column"):
                contact_enabled = notifications_enabled()
                forwarding = gr.Checkbox(
                    label="Allow unanswered questions to be sent to Kaushik via Pushover",
                    value=False, visible=contact_enabled,
                )
                conversation = gr.ChatInterface(
                    fn=chat,
                    examples=[[prompt] for prompt in EXAMPLES if contact_enabled or prompt != CONTACT_PROMPT],
                    additional_inputs=[forwarding],
                    cache_examples=False,
                    chatbot=gr.Chatbot(show_label=False, height=510, elem_id="twin-chatbot"),
                    textbox=gr.Textbox(
                        placeholder="Ask a question or follow up…",
                        elem_id="twin-input",
                        submit_btn="Send",
                        stop_btn=True,
                        autofocus=True,
                    ),
                )
            with gr.Column(scale=1, min_width=235, elem_id="twin-explorer"):
                gr.Markdown(
                    "## Project Explorer\nChoose a project to start a question.",
                    elem_id="twin-project-heading",
                )
                gr.Markdown("### Featured projects", elem_id="twin-featured-heading")
                for title, stack, question in PROJECT_GROUPS[0][1]:
                    with gr.Column(elem_classes="twin-project"):
                        button = gr.Button(title, size="sm", elem_classes="twin-project-link")
                        gr.Markdown(stack, elem_classes="twin-stack")
                        button.click(
                            fn=lambda draft=question: draft,
                            outputs=conversation.textbox,
                            queue=False,
                            show_progress="hidden",
                            api_visibility="undocumented",
                        )
        if notifications_enabled():
            with gr.Accordion("Contact Kaushik", open=False):
                gr.Markdown("Review your email and message below. Confirm and send forwards both to Kaushik via Pushover.")
                email = gr.Textbox(label="Your email")
                note = gr.Textbox(label="Your message (optional)")
                confirm = gr.Button("Confirm and send")
                status = gr.Textbox(label="Delivery status", interactive=False)
                confirm.click(send_contact, inputs=[email, note], outputs=status)
    return demo


def build_theme():
    colors = {
        "body_background_fill": "#111b26",
        "body_text_color": "#f0f5fa",
        "body_text_color_subdued": "#b9c5d2",
        "background_fill_primary": "#16222f",
        "background_fill_secondary": "#263746",
        "border_color_primary": "#354657",
        "block_background_fill": "#1d2937",
        "block_border_color": "#354657",
        "input_background_fill": "#1d2937",
        "input_border_color": "#526577",
        "button_primary_background_fill": "#a9e3c8",
        "button_primary_background_fill_hover": "#c6f2de",
        "button_primary_text_color": "#152322",
        "button_secondary_background_fill": "#223142",
        "button_secondary_background_fill_hover": "#304659",
        "button_secondary_text_color": "#f0f5fa",
        "link_text_color": "#a9e3c8",
    }
    return gr.themes.Base().set(**colors, **{f"{key}_dark": value for key, value in colors.items()})


if __name__ == "__main__":
    build_demo().launch(
        server_name=os.getenv("HOST", "127.0.0.1"),
        server_port=int(os.getenv("PORT", "7860")),
        css=CSS,
        js=JS,
        theme=build_theme(),
        share=os.getenv("GRADIO_SHARE", "").strip().lower() in {"1", "true"},
    )
