from fastapi import FastAPI
from pydantic import BaseModel, Field

# Reuse the existing meeting summary agent logic.
# Importing is safe: the interactive CLI is guarded by `if __name__ == "__main__"`.
from meeting_summary_agent import (
    SAMPLES,
    summarise,
    extract_actions,
    identify_owners,
    draft_email,
)

app = FastAPI(title="Meeting Summary API")


class MeetingRequest(BaseModel):
    title: str = Field(default="Untitled Meeting", description="Title of the meeting")
    notes: str = Field(..., description="Raw meeting notes to summarise")


class MeetingResponse(BaseModel):
    title: str
    summary: str
    action_items: str
    owners: str
    follow_up_email: str


@app.get("/")
def home():
    return {
        "message": "Meeting Summary API",
        "endpoints": ["POST /summarise-meeting"],
        "samples": {key: sample["title"] for key, sample in SAMPLES.items()},
    }


@app.post("/summarise-meeting", response_model=MeetingResponse)
def summarise_meeting(request: MeetingRequest):
    notes = request.notes
    title = request.title or "Untitled Meeting"

    summary = summarise(notes)
    action_items = extract_actions(notes)
    owners = identify_owners(action_items)
    follow_up_email = draft_email(title, summary, action_items)

    return MeetingResponse(
        title=title,
        summary=summary,
        action_items=action_items,
        owners=owners,
        follow_up_email=follow_up_email,
    )
