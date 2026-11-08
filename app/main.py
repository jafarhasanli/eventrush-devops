from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="EventRush API", version="0.1.0")

class Event(BaseModel):
    id: int
    title: str
    capacity: int = Field(ge=0)

_DEMO_EVENTS = [Event(id=1, title="Demo Concert", capacity=500)]

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/events", response_model=list[Event])
def list_events() -> list[Event]:
    return _DEMO_EVENTS
