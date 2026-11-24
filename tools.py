import json
import os
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


def record_user_details(email, name="Name not provided", notes="not provided"):
    return push(f"Recording interest from {name} with email {email} and notes {notes}")


def record_unknown_question(question):
    return push(f"Recording {question} asked that I couldn't answer")


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and consented to sharing their email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {
                "type": "string",
                "description": "Any additional info about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

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
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]

tool_map = {
    "record_user_details": record_user_details,
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
