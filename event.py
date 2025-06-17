from fastapi import FastAPI, File, UploadFile, Form, HTTPException,Response
from datetime import datetime, time, timedelta,date
from typing import Annotated
from uuid import UUID, uuid4
from pydantic import BaseModel
from typing import Optional

from typing import List

app = FastAPI()


class Event(BaseModel):
    id: str
    title: str
    location: str
    speaker_name :str
    speaker_topic : str
    is_open: bool 
    date: date
   

class EventCreate(BaseModel):
     title: str
     location: str
     speaker_name :str
     speaker_topic : str
     is_open: bool 
     date: date

class EventUpdate(BaseModel):
     title: str
     location: str
     speaker_name :str
     speaker_topic : str
     is_open: bool 
     date: date

class CloseEventReg(BaseModel):

    is_open : bool = False

class Events(BaseModel):
    event: list[Event]


class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None
    data: Optional[Event | Events] = None


event_db: dict[str, Event] = {}


@app.get("/events")
def get_events():
    return event_db

@app.post("/events")
def add_event(event_in: EventCreate):
    event = Event(
        id=str(UUID(int=len(event_db) + 3)),
        **event_in.model_dump(),
    )
    event_db[event.id] = event
    return Response(message="Event added successfully", data=event)


@app.put("/events/{id}")
def event_update(id: UUID, event_in: EventUpdate):
    event = event_db.get(str(id))
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.title = event_in.title
    event.location = event_in.location
    event.speaker_name = event_in.speaker_name
    event.speaker_topic = event_in.speaker_topic
    event.date = event_in.date
    return Response(message="Event updated successfully", data=event)


@app.patch("/events/{id}")
def close_event_registration(id: UUID, event_in: CloseEventReg):
    event = event_db.get(str(id))
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.is_open = event_in.is_open

    return Response(message=" Event closed successfully", data=event)


@app.delete("/events/{id}")
def delete_event(id: UUID):
    event = event_db.get(str(id))
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    del event_db[event.id]

    return Response(message="Event deleted successfully")





    
    

