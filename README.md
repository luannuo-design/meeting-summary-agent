# Meeting Summary Agent

An AI agent that turns raw meeting notes into a clean summary, a list of action
items, an owners table, and a ready-to-send follow-up email. Powered by the
Anthropic Claude API.

It can be used two ways:

- **CLI** — an interactive script with built-in sample meetings (`meeting_summary_agent.py`)
- **HTTP API** — a FastAPI service exposing a `POST /summarise-meeting` endpoint (`api.py`)

## What it does

Given meeting notes, the agent runs four steps in sequence:

1. **Summarise** — 3–5 bullet points capturing the meeting.
2. **Extract action items** — a numbered list with deadlines where mentioned.
3. **Identify owners** — a markdown table of `Owner | Action | Deadline`.
4. **Draft follow-up email** — a short, professional recap email.

## Requirements

- Python 3.9+
- An Anthropic API key
- Packages: `anthropic`, `fastapi`, `uvicorn`, `pydantic` (only needed for the API)

```bash
pip install anthropic fastapi uvicorn pydantic
```

## Setup

Set your Anthropic API key as an environment variable.

PowerShell (Windows):

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

bash / zsh (macOS, Linux):

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Usage

### CLI

```bash
python meeting_summary_agent.py
```

You'll be prompted to pick one of four built-in sample meetings, or to paste
your own notes (type `END` on its own line when finished). The summary, action
items, owners table, and follow-up email are printed to the terminal.

### API

Start the server:

```bash
python -m uvicorn api:app --reload
```

> Note: use `python -m uvicorn` if the bare `uvicorn` command isn't on your PATH.

The service runs at `http://127.0.0.1:8000`. Interactive docs (Swagger UI) are
available at `http://127.0.0.1:8000/docs`.

#### Endpoints

| Method | Path                  | Description                                   |
|--------|-----------------------|-----------------------------------------------|
| GET    | `/`                   | API info and the list of built-in samples     |
| POST   | `/summarise-meeting`  | Summarise meeting notes and return the results |

#### `POST /summarise-meeting`

Request body:

```json
{
  "title": "Weekly Engineering Standup",
  "notes": "Alice finished the payment API. Ben will fix two frontend bugs by Friday..."
}
```

`title` is optional (defaults to `"Untitled Meeting"`); `notes` is required.

Response:

```json
{
  "title": "Weekly Engineering Standup",
  "summary": "- Alice completed the payment API integration...",
  "action_items": "1. James to complete code review...",
  "owners": "| Owner | Action | Deadline |\n|-------|--------|----------|\n...",
  "follow_up_email": "Subject: Follow-Up: Weekly Engineering Standup..."
}
```

#### Example request

PowerShell:

```powershell
$body = @{
  title = "Weekly Engineering Standup"
  notes = "Alice finished the payment API. Ben will fix two frontend bugs by Friday. Carmen filed three bugs in Jira today."
} | ConvertTo-Json

Invoke-RestMethod -Uri http://127.0.0.1:8000/summarise-meeting -Method Post -Body $body -ContentType "application/json"
```

curl:

```bash
curl -X POST http://127.0.0.1:8000/summarise-meeting \
  -H "Content-Type: application/json" \
  -d '{"title":"Weekly Engineering Standup","notes":"Alice finished the payment API. Ben will fix two frontend bugs by Friday."}'
```

## Notes

- Each request to `/summarise-meeting` makes four sequential Claude calls, so
  expect a few seconds of latency per request.
- The model is set via the `MODEL` constant in `meeting_summary_agent.py`.
