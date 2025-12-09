from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List

from ..database import get_session
from ..models import Notification, UserProfile
from ..auth import get_current_user

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=List[Notification])
def get_notifications(
    current_user: UserProfile = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Listar notificações do usuário"""
    notifications = session.exec(
        select(Notification)
        .where(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
    ).all()
    return notifications


@router.post("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    current_user: UserProfile = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Marcar notificação como lida"""
    notification = session.get(Notification, notification_id)
    if not notification or notification.user_id != current_user.id:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    
    notification.read = True
    session.add(notification)
    session.commit()
    return {"status": "ok"}


@router.get("/unread/count")
def unread_count(
    current_user: UserProfile = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Contar notificações não lidas"""
    count = len(session.exec(
        select(Notification)
        .where(Notification.user_id == current_user.id)
        .where(Notification.read == False)
    ).all())
    return {"count": count}
