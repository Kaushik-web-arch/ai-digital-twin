"""Capture actual Gemini responses and review them offline."""
from datetime import datetime
from html import escape
from pathlib import Path

from app import MODEL_NAME, chat


def main():
    checks = [
        ("Who built sih103?", "Kaushik was its sole developer."),
        ("What did that project monitor?", "Government infrastructure projects using monthly reports."),
        ("What did Ghost Drain Hunter win, and what was Kaushik's role?",
         "Team third prize at DAEMON HOUR. Screen event monitoring, local storage and Android integration."),
        ("Which Nobel Prize did Kaushik win?", "The profile provides no evidence of a Nobel Prize."),
    ]
    stamp = datetime.now()
    output = Path(__file__).with_name(stamp.strftime("review-%Y%m%d-%H%M%S-%f.html"))
    sections = ["<!doctype html><meta charset=utf-8><title>AI Twin demo review</title>",
                "<style>body{max-width:48rem;margin:3rem auto;padding:0 1rem;font:17px/1.5 system-ui}article{white-space:pre-wrap}</style>",
                "<h1>AI Twin demo review</h1>", escape(f"{stamp:%Y-%m-%d %H:%M} | {MODEL_NAME}")]
    history = []
    for index, (question, expected) in enumerate(checks):
        if index != 1:
            history = []
        try:
            answer = chat(question, history)
        except Exception as error:
            sections.append(f"<h2>{escape(question)}</h2><p>Request failed: {escape(str(error))}</p>")
            output.write_text("\n".join(sections), encoding="utf-8")
            raise SystemExit(f"Stopped. See {output}") from None
        history.extend([{"role": "user", "content": question}, {"role": "assistant", "content": answer}])
        sections.append(f"<h2>{escape(question)}</h2><article>{escape(answer)}</article><p><b>Check against:</b> {escape(expected)}</p>")
        output.write_text("\n".join(sections), encoding="utf-8")
    print(f"Review all four answers in {output}")


if __name__ == "__main__":
    main()
