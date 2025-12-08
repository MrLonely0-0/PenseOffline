from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from ..database import get_session
from ..models import Event, XPHistory, UserProfile
from ..auth import get_current_user

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_model=List[Event])
def list_events(session: Session = Depends(get_session)):
    return session.exec(select(Event)).all()


@router.post("/", response_model=Event)
def create_event(data: Event, current_user: UserProfile = Depends(get_current_user), session: Session = Depends(get_session)):
    data.creator_id = current_user.id
    session.add(data)
    session.commit()
    session.refresh(data)
    return data


@router.get("/{event_id}", response_model=Event)
def get_event(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/{event_id}/attend")
def attend_event(event_id: int, current_user: UserProfile = Depends(get_current_user), session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    # award xp
    xp = event.xp_reward or 0
    current_user.adicionar_pontos(xp)
    session.add(current_user)
    history = XPHistory(user_id=current_user.id, event_id=event.id, type="event", xp_amount=xp)
    session.add(history)
    session.commit()
    session.refresh(current_user)
    return {"message": "Event marked as attended", "xp_awarded": xp, "total_xp": current_user.xp_total}
