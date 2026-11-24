import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
import requests
from urllib.parse import quote

from context import TWIN_SYSTEM_PROMPT
from styles import CSS, EXAMPLES, JS, PROJECT_GROUPS
from tools import tool_map, notifications_enabled, tools

load_dotenv(Path(__file__).with_name(".env"))

MODEL_NAME = os.getenv("GEMINI_MODEL", "").strip() or "gemini-3.5-flash-lite"
API_ROOT = "https://generativelanguage.googleapis.com/v1beta/models"
MAX_TOOL_ROUNDS = 3


def generate(model, payload, key):
    try:
        response = requests.post(
            f"{API_ROOT}/{quote(model, safe='')}:generateContent",
            headers={"x-goog-api-key": key}, json=payload, timeout=(5, 20),
        )
    except requests.Timeout:
        raise gr.Error("The Gemini request timed out. Please try again.") from None
    except requests.ConnectionError:
        raise gr.Error("Could not connect to Google. Check the connection to generativelanguage.googleapis.com.") from None
    return response


def chat(message, history):
    key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not key or key == "your_google_gemini_api_key_here":
        raise gr.Error("Set GOOGLE_API_KEY in .env and restart.")
    if not message.strip():
        raise gr.Error("Enter a question.")

    contents = []
    for item in history:
        text = item.get("content")
        if isinstance(text, list):
            text = "\n".join(p["text"] for p in text if isinstance(p, dict)
                              and p.get("type") == "text" and isinstance(p.get("text"), str))
        if item.get("role") in {"assistant", "user"} and isinstance(text, str) and text.strip():
            role = "model" if item["role"] == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": text}]})
    contents.append({"role": "user", "parts": [{"text": message}]})
    system = TWIN_SYSTEM_PROMPT
    enabled = notifications_enabled()
    if not enabled:
        system += "\nNotifications are disabled. Explain that forwarding is unavailable if asked."
    payload = {"systemInstruction": {"parts": [{"text": system}]}, "contents": contents}
    if enabled:
        declarations = [
            {"name": spec["name"], "description": spec["description"],
             "parametersJsonSchema": spec["parameters"]}
            for spec in (entry["function"] for entry in tools)
        ]
        payload["tools"] = [{"functionDeclarations": declarations}]

    model = MODEL_NAME
    for attempt in range(MAX_TOOL_ROUNDS + 1):
        response = generate(model, payload, key)
        if attempt == 0 and response.status_code in (404, 503) and model != "gemini-flash-latest":
            print(f"{model} returned HTTP {response.status_code}. Trying gemini-flash-latest.", flush=True)
            model = "gemini-flash-latest"
            response = generate(model, payload, key)
        if not response.ok:
            print(f"Native Gemini request: {model}, HTTP {response.status_code}", flush=True)
            raise gr.Error(f"Google returned HTTP {response.status_code} for {model}.")
        data = response.json()
        candidate = next(iter(data.get("candidates", [])), {})
        reply = candidate.get("content", {})
        parts = reply.get("parts", [])
        calls = [part["functionCall"] for part in parts if part.get("functionCall")]
        if not calls:
            answer = "\n".join(p["text"] for p in parts if p.get("text") and not p.get("thought"))
            if answer.strip():
                return answer
            break
        if not enabled or attempt == MAX_TOOL_ROUNDS:
            break
        contents.append(reply)
        results = []
        for call in calls:
            name = call["name"]
            try:
                result = tool_map[name](**call.get("args", {}))
            except (KeyError, TypeError):
                result = {"status": "invalid_tool_call"}
            result_part = {"name": name, "response": result}
            if call.get("id"):
                result_part["id"] = call["id"]
            results.append({"functionResponse": result_part})
        contents.append({"role": "user", "parts": results})
    raise gr.Error("Gemini returned no text answer. Try rephrasing your question.")


def build_demo():
    with gr.Blocks(title="Kaushik Santhosh | Digital Twin") as demo:
        gr.Markdown(
            "# Kaushik Santhosh\nAI Digital Twin · Projects, skills and experience",
            elem_id="twin-header",
        )
        with gr.Row(elem_id="twin-layout"):
            with gr.Column(scale=3, elem_id="twin-chat-column"):
                conversation = gr.ChatInterface(
                    fn=chat,
                    examples=EXAMPLES,
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
