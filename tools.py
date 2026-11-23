import json
import os
import re
import requests
pushover_url = "https://api.pushover.net/1/messages.json"


def notifications_enabled():
    return bool(os.getenv("PUSHOVER_USER", "").strip() and os.getenv("PUSHOVER_TOKEN", "").strip())


def push(text):
    """Send a Pushover notification and report whether the service accepted it."""
    if not notifications_enabled():
        return {"status": "disabled"}

    try:
        response = requests.post(
            pushover_url,
            data={
                "token": os.environ["PUSHOVER_TOKEN"].strip(),
                "user": os.environ["PUSHOVER_USER"].strip(),
                "message": text,
            },
            timeout=10,
        )
        response.raise_for_status()
        if response.json().get("status") == 1:
            return {"status": "accepted"}
    except (requests.RequestException, ValueError):
        pass
    return {"status": "failed"}


def send_contact(email, notes):
    email = email.strip()
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        return "Enter a valid email address."
    message = f"Contact request from {email}\n{notes.strip()}"
    if len(message) > 1024:
        return "Please shorten your message and try again."
    outcome = push(message)["status"]
    return {"accepted": "Pushover accepted your message.", "disabled": "Contact is disabled.",
            "failed": "Delivery failed. Please try again."}[outcome]


def record_unknown_question(question):
    return push(f"Recording {question} asked that I couldn't answer")


record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_unknown_question_json},
]

tool_map = {
    "record_unknown_question": record_unknown_question,
}


def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool = tool_map.get(tool_name)
        try:
            arguments = json.loads(tool_call.function.arguments)
            result = tool(**arguments) if tool else {"status": "unknown_tool"}
        except (ValueError, TypeError):
            result = {"status": "invalid_arguments"}
        results.append(
            {"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id}
        )
    return results
