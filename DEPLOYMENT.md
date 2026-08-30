# Live Demo Deployment

The repository is prepared to run as a hosted Gradio application.

## Recommended: Railway

1. In Railway, create a new project.
2. Choose **Deploy from GitHub repo**.
3. Select `Kaushik-web-arch/ai-digital-twin`.
4. In the service **Variables** tab, add:

```text
GOOGLE_API_KEY=<your Gemini API key>
```

Optional notification variables:

```text
PUSHOVER_USER=<optional>
PUSHOVER_TOKEN=<optional>
```

5. Deploy the service.
6. Open the service **Settings → Networking → Generate Domain**.
7. Copy the generated public URL.
8. Add that URL to the `Live demo` section of `README.md`.

The application already binds to `0.0.0.0` and reads Railway's `PORT` environment variable automatically.

## Security

- Never commit `.env`.
- Never put the Gemini API key directly in Python files or README files.
- Store production credentials only as hosting-platform secrets/environment variables.
