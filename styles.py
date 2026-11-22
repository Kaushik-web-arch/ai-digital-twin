"""Project Explorer styling and conversation starters for the Digital Twin."""

PROJECTS = (
    ("AI Research Agent", "Gemini · Gradio", "How does the AI Research Agent turn a topic into a report with sources?"),
    ("Student Placement Portal", "Flask · MySQL", "How do the admin and student workflows connect in the Student Placement Portal?"),
    ("Zen Sports & Fitness", "Streamlit · SQLite", "How does the Zen Sports & Fitness app handle belt grading and certificates?"),
    ("FinSight", "Streamlit · Scikit-learn", "How does FinSight forecast expenses and flag unusual spending?"),
)

EXAMPLES = [
    "👋 Tell me about Kaushik",
    "💻 What are his strongest technical skills?",
    "🤖 What is he learning about AI?",
    "🚀 What projects and experiences has he worked on?",
    "🎓 Tell me about his education",
    "📩 How can I get in touch with him?",
    *(question for _, _, question in PROJECTS),
    "How does this AI Digital Twin use Kaushik’s profile to answer questions?",
]

CSS = """
html, body, gradio-app {
    background: #111b26;
    color-scheme: dark;
}

.gradio-container {
    max-width: 1240px !important;
    margin-inline: auto !important;
    padding: 24px clamp(14px, 3vw, 36px) 32px !important;
}

#twin-header {
    border-bottom: 1px solid #354657;
    padding: 4px 0 17px;
    margin-bottom: 4px;
}

#twin-header h1 {
    color: #f0f5fa;
    margin: 0 0 5px;
    font-size: clamp(26px, 4vw, 36px);
    letter-spacing: -.035em;
}

#twin-header p, #twin-project-heading p, .twin-stack p {
    color: #b9c5d2;
    margin: 0;
}

#twin-layout { gap: 20px; align-items: start; }
#twin-chat-column { min-width: 0 !important; }
#twin-chatbot { border-color: #354657; }

#twin-chatbot .user {
    background: #a9e3c8;
    color: #152322;
}

#twin-chatbot .user :is(p, li, strong, code) {
    color: inherit;
}

#twin-chatbot button:focus-visible,
#twin-explorer button:focus-visible,
#twin-input textarea:focus-visible {
    outline: 2px solid #a9e3c8;
    outline-offset: 3px;
}

#twin-explorer {
    background: #16222f;
    border: 1px solid #354657;
    border-radius: 12px;
    padding: 18px;
    gap: 0;
}

#twin-project-heading { padding-bottom: 14px; }
#twin-project-heading h2 { margin: 0 0 7px; font-size: 19px; }
.twin-project { border-top: 1px solid #354657; padding: 10px 0; gap: 1px; }

button.twin-project-link {
    justify-content: flex-start;
    text-align: left;
    background: transparent;
    border: 0;
    box-shadow: none;
    color: #edf5fa;
    padding: 4px 6px;
}

button.twin-project-link:hover {
    background: #263746;
    color: #a9e3c8;
}

.twin-stack { padding: 0 6px; font-size: 13px; }
footer { display: none !important; }

@media (max-width: 800px) {
    #twin-layout { flex-direction: column; }
    #twin-chat-column, #twin-explorer { width: 100%; min-width: 0 !important; }
    #twin-chatbot { max-height: 60dvh; }
}
"""

JS = """
() => {
    document.title = "Kaushik Santhosh | Digital Twin";
    document.addEventListener("keydown", event => {
        if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
            const input = document.querySelector("#twin-input textarea");
            if (input) {
                event.preventDefault();
                input.focus();
            }
        }
    });
}
"""
