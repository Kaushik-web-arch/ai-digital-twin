"""Project Explorer styling and conversation starters for the Digital Twin."""

PROJECTS = (
    ("AI Research Agent", "Gemini · Gradio", "How does the AI Research Agent turn a topic into a report with sources?"),
    ("Student Placement Portal", "Flask · MySQL", "How do the admin and student workflows connect in the Student Placement Portal?"),
    ("Zen Sports & Fitness", "Streamlit · SQLite", "How does the Zen Sports & Fitness app handle belt grading and certificates?"),
    ("FinSight", "Streamlit · Scikit-learn", "How does FinSight forecast expenses and flag unusual spending?"),
)

PROJECT_GROUPS = (
    (
        "Featured projects",
        (
            ("AI Digital Twin", "Gemini · Gradio · PyPDF", "How does this AI Digital Twin use Kaushik’s profile to answer questions?"),
            ("Multi-Model SDR Outreach Agent", "Prototype · Gemini · Groq", "How does Kaushik’s Multi-Model SDR Outreach Agent draft and review outreach emails?"),
            ("sih103", "Infrastructure monitoring · React · FastAPI", "What did Kaushik build as the sole developer of sih103?"),
            ("Ghost Drain Hunter", "DAEMON HOUR · Third prize · Kotlin", "What did Kaushik build for the battery app that won third prize at DAEMON HOUR?"),
            *PROJECTS,
        ),
    ),
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

#twin-header p, #twin-project-heading p, #twin-featured-heading p, .twin-stack p {
    color: #b9c5d2;
    margin: 0;
}

#twin-layout { gap: 20px; align-items: start; }
#twin-chat-column { min-width: 0 !important; flex: 1 1 0 !important; }
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
    box-sizing: border-box;
    background: #16222f;
    border: 1px solid #354657;
    border-radius: 12px;
    padding: 14px;
    gap: 8px;
    width: 260px !important;
    min-width: 235px !important;
    max-width: 275px !important;
    flex: 0 0 260px !important;
    max-height: min(650px, 80dvh);
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-color: #526577 #16222f;
}

#twin-explorer > * {
    box-sizing: border-box;
    min-width: 0 !important;
    max-width: 100% !important;
}

#twin-project-heading { padding-bottom: 3px; }
#twin-project-heading h2 { margin: 0 0 6px; font-size: 19px; }
#twin-featured-heading { padding: 2px 6px 4px; }
#twin-featured-heading h3 {
    margin: 0;
    color: #a9e3c8;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: .06em;
    text-transform: uppercase;
}
.twin-project {
    box-sizing: border-box;
    width: 100%;
    min-width: 0;
    border-top: 1px solid #354657;
    padding: 8px 0;
    gap: 2px;
}

button.twin-project-link {
    box-sizing: border-box;
    width: 100%;
    max-width: 100%;
    min-width: 0;
    justify-content: flex-start;
    text-align: left;
    white-space: normal !important;
    overflow-wrap: anywhere;
    background: transparent;
    border: 0;
    box-shadow: none;
    color: #edf5fa;
    padding: 5px 6px;
    font-size: 13px;
    line-height: 1.35;
}

button.twin-project-link:hover {
    background: #263746;
    color: #a9e3c8;
}

.twin-stack {
    box-sizing: border-box;
    max-width: 100%;
    padding: 0 6px;
    font-size: 11px;
    overflow-wrap: anywhere;
    word-break: break-word;
}
footer { display: none !important; }

@media (max-width: 800px) {
    #twin-layout { flex-direction: column; }
    #twin-chat-column, #twin-explorer {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        flex: 1 1 auto !important;
    }
    #twin-chatbot { max-height: 60dvh; }
    #twin-explorer {
        max-height: 420px;
        overflow-x: hidden;
    }
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
