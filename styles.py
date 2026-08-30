"""UI styling and suggested questions for the Digital Twin."""

EXAMPLES = [
    "👋 Tell me about Kaushik",
    "💻 What are his strongest technical skills?",
    "🤖 What is he learning about AI?",
    "🚀 What projects and experiences has he worked on?",
    "🎓 Tell me about his education",
    "📩 How can I get in touch with him?",
]

CSS = r"""
:root {
    --gold: #F5B942;
    --blue: #3B82F6;
    --purple: #8B5CF6;
    --bg: #080A0F;
    --surface: rgba(18, 22, 32, 0.92);
    --border: rgba(255,255,255,0.10);
    --text: #F4F6FA;
    --muted: #A6B0C0;
}

html, body, gradio-app {
    background:
        radial-gradient(circle at 15% 10%, rgba(59,130,246,0.12), transparent 34%),
        radial-gradient(circle at 90% 15%, rgba(139,92,246,0.12), transparent 34%),
        var(--bg) !important;
    color: var(--text) !important;
}

.gradio-container {
    max-width: 1000px !important;
    margin: 0 auto !important;
    padding: 38px 18px 52px !important;
}

.gradio-container h1 {
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
}

.chatbot, .chatbot.block {
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    background: var(--surface) !important;
    box-shadow: 0 28px 70px rgba(0,0,0,0.35) !important;
}

textarea, input[type="text"] {
    border-radius: 14px !important;
}

button.primary, button.submit, button.submit-button {
    background: linear-gradient(135deg, var(--gold), #F7C95D) !important;
    color: #111318 !important;
    border: none !important;
}

.examples button, [data-testid="examples"] button {
    border-radius: 999px !important;
    border: 1px solid var(--border) !important;
    background: rgba(255,255,255,0.04) !important;
}

footer, .built-with, .show-api, .api-docs {
    display: none !important;
}
"""

JS = r"""
() => {
    document.title = "Kaushik Santhosh | Digital Twin";
    const focusInput = () => {
        const boxes = document.querySelectorAll("textarea");
        if (boxes.length) boxes[boxes.length - 1].focus();
    };
    setTimeout(focusInput, 500);
    document.addEventListener("keydown", event => {
        if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
            event.preventDefault();
            focusInput();
        }
    });
}
"""
