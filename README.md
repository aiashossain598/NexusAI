<h1 align="center">
  <br>
  🤖 NexusAI
  <br>
</h1>

<p align="center">
  <b>An open-source, self-hosted AI coding assistant with a secure agent core and a beautiful cross-platform UI.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-0.1.0-009688?logo=fastapi" />
  <img src="https://img.shields.io/badge/Flutter-3.x-02569B?logo=flutter" />
  <img src="https://img.shields.io/badge/Gemini-2.5--flash-4285F4?logo=google" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

---

## Overview

NexusAI is a multi-component AI coding assistant platform. It pairs a **FastAPI Python backend** (the "Core") that runs a sandboxed agentic loop with a **Flutter cross-platform desktop client** (Windows, macOS, Linux, iOS, Android, Web).

The agent can read files, write files, list directories, and run shell commands — all within a policy-enforced workspace sandbox that requires explicit human confirmation before any destructive or privileged operation.

---

## Architecture

```
nexus_desktop (Flutter UI)
       |
       |  REST /api/chat  +  WebSocket
       ▼
nexus-core (FastAPI)
  ├── CodingAgent loop (≤15 turns)
  │     ├── GeminiModelClient  (gemini-2.5-flash)
  │     └── LocalFallbackModelClient
  ├── ToolExecutor
  │     ├── read_file
  │     ├── write_file
  │     ├── list_directory
  │     └── run_shell
  ├── WorkspacePolicy  (path sandboxing + shell safety)
  ├── ConfirmationManager  (human-in-the-loop approvals)
  ├── MemoryManager  (per-session conversation history)
  └── EventBus  (pub/sub observability)
```

---

## Repository Structure

| Module | Status | Description |
|---|---|---|
| `nexus-core/` | ✅ Active | Python / FastAPI backend & agent core |
| `nexus_desktop/` | ✅ Active | Flutter cross-platform UI |
| `nexus-api/` | 🚧 Planned | Standalone REST API gateway |
| `nexus-agents/` | 🚧 Planned | Dedicated agents service |
| `nexus-sdk/` | 🚧 Planned | Client SDK |
| `nexus-plugins/` | 🚧 Planned | Plugin marketplace |
| `nexus-mobile/` | 🚧 Planned | Mobile-first client |

---

## Getting Started

### Prerequisites

- Python 3.12+
- Flutter SDK 3.12+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey) (or run without for local fallback mode)

### 1. Backend — `nexus-core`

```bash
cd nexus-core

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.development .env
# Edit .env and add your GEMINI_API_KEY

# Start the server
uvicorn app.server:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.
Interactive docs: `http://localhost:8000/docs`

### 2. Desktop UI — `nexus_desktop`

```bash
cd nexus_desktop
flutter pub get
flutter run -d windows   # or macos / linux / chrome
```

---

## API Reference

### Chat

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/chat` | Send a message to the AI agent |
| `POST` | `/api/chat/confirm` | Approve or reject a pending tool action |
| `GET` | `/api/chat/history/{session_id}` | Retrieve conversation history |
| `WS` | `/ws` | Real-time streaming WebSocket |

**Example request:**
```json
POST /api/chat
{
  "instruction": "List all Python files in the project",
  "session_id": "my-session"
}
```

### Health

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Liveness check |
| `GET` | `/system` | System info |

---

## Authentication

Set `NEXUS_API_KEY` in your `.env` to enable API key authentication:

```env
NEXUS_API_KEY=your-secret-key-here
```

All requests (except `/health`, `/docs`, `/`) must then include:
```
X-API-Key: your-secret-key-here
```

If `NEXUS_API_KEY` is not set, auth is disabled (development mode).

---

## Security Model

NexusAI implements a defence-in-depth security model for agent tool execution:

| Control | Detail |
|---|---|
| **Workspace sandboxing** | All file operations are restricted to the configured workspace directory. Path traversal attempts are hard-blocked. |
| **Protected files** | `.env`, `.git`, and related secrets are inaccessible to agents. |
| **Shell command policy** | Destructive commands (`rm`, `del`, `format`, etc.) and shell control operators require explicit human confirmation. |
| **Human-in-the-loop** | Confirmation tokens are cryptographically random. The model cannot self-approve actions. |
| **Env key scrubbing** | `GEMINI_API_KEY` and `OPENAI_API_KEY` are stripped from subprocess environments. |
| **Output truncation** | Tool outputs are capped at 8,000 characters to prevent context flooding. |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Recommended | Google Gemini API key. If absent, local fallback model is used. |
| `NEXUS_GEMINI_MODEL` | Optional | Override Gemini model name (default: `gemini-2.5-flash`) |
| `NEXUS_API_KEY` | Optional | API key for request authentication (disabled if not set) |
| `APP_ENV` | Optional | `development` / `production` / `testing` (default: `development`) |

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License

MIT
