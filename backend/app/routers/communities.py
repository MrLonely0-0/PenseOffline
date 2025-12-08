from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from ..database import get_session
from ..models import Community, CommunityMembership, UserProfile
from ..auth import get_current_user

router = APIRouter(prefix="/communities", tags=["communities"])


@router.get("/", response_model=List[Community])
def list_communities(session: Session = Depends(get_session)):
    return session.exec(select(Community)).all()


@router.post("/", response_model=Community)
def create_community(data: Community, current_user: UserProfile = Depends(get_current_user), session: Session = Depends(get_session)):
    data.owner_id = current_user.id
    session.add(data)
    session.commit()
    session.refresh(data)
    return data


@router.get("/{community_id}", response_model=Community)
def get_community(community_id: int, session: Session = Depends(get_session)):
    comm = session.get(Community, community_id)
    if not comm:
        raise HTTPException(status_code=404, detail="Community not found")
    return comm


@router.post("/{community_id}/join")
def join_community(community_id: int, current_user: UserProfile = Depends(get_current_user), session: Session = Depends(get_session)):
    comm = session.get(Community, community_id)
    if not comm:
        raise HTTPException(status_code=404, detail="Community not found")
    # Check existing membership
    existing = session.exec(select(CommunityMembership).where(CommunityMembership.community_id == community_id, CommunityMembership.user_id == current_user.id)).first()
    if existing:
        return {"message": "Already member"}
    membership = CommunityMembership(community_id=community_id, user_id=current_user.id)
    session.add(membership)
    session.commit()
    session.refresh(membership)
    return {"message": "Joined", "membership_id": membership.id}


@router.post("/{community_id}/leave")
def leave_community(community_id: int, current_user: UserProfile = Depends(get_current_user), session: Session = Depends(get_session)):
    membership = session.exec(select(CommunityMembership).where(CommunityMembership.community_id == community_id, CommunityMembership.user_id == current_user.id)).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Not a member")
    session.delete(membership)
    session.commit()
    return {"message": "Left"}
