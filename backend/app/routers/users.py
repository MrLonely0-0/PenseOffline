from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlmodel import Session, select
from typing import List, Optional
import re

from ..database import get_session
from ..models import UserProfile, UserPublic, UserCreate, UserLogin, Token, XPHistory
from ..auth import get_current_user, hash_password, verify_password, create_access_token, user_to_public

router = APIRouter(prefix="/users", tags=["users"])


def validate_username(username: str) -> tuple[bool, str]:
    """Validar username como @instagram (alfanumérico, _, hífem; sem espaços)"""
    if not username or len(username) < 3 or len(username) > 30:
        return False, "Username deve ter entre 3 e 30 caracteres"
    if not re.match(r"^[a-zA-Z0-9_-]+$", username):
        return False, "Username pode conter apenas letras, números, underscore (_) e hífen (-)"
    return True, ""


def validate_email(email: str) -> tuple[bool, str]:
    """Validar email básico"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, "Email inválido"
    return True, ""


@router.get("/me", response_model=UserPublic)
def me(current_user: UserProfile = Depends(get_current_user)):
    return user_to_public(current_user)


@router.get("/{user_id}", response_model=UserPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(UserProfile, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_to_public(user)


@router.get("", response_model=List[UserPublic])
def list_users(current_user: UserProfile = Depends(get_current_user), session: Session = Depends(get_session)):
    """Listar todos os usuários para ranking (requer autenticação)"""
    users = session.exec(select(UserProfile).order_by(UserProfile.pontos.desc())).all()
    return [user_to_public(user) for user in users]


@router.post("/register", response_model=Token, status_code=201)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    # Validar username (como @instagram)
    valid, msg = validate_username(user_data.username)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)
    
    # Validar email
    valid, msg = validate_email(user_data.email)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)
    
    # Verificar username único (case-insensitive)
    existing_user = session.exec(
        select(UserProfile).where(UserProfile.username.ilike(user_data.username))
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '@{user_data.username}' já está em uso"
        )
    
    # Verificar email único (case-insensitive)
    existing_email = session.exec(
        select(UserProfile).where(UserProfile.email.ilike(user_data.email))
    ).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já está cadastrado"
        )
    
    # Criar novo usuário
    user = UserProfile(
        username=user_data.username,
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hash_password(user_data.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    
    token = create_access_token({"sub": user.username})
    return Token(access_token=token, token_type="bearer", user=user_to_public(user))




@router.post("/login", response_model=Token)
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(UserProfile).where(UserProfile.username.ilike(credentials.username))).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Username ou senha incorretos")
    from datetime import datetime
    user.ultimo_acesso = datetime.utcnow()
    session.add(user)
    session.commit()
    token = create_access_token({"sub": user.username})
    return Token(access_token=token, token_type="bearer", user=user_to_public(user))


@router.get("/me/xp_history", response_model=List[XPHistory])
def xp_history(current_user: UserProfile = Depends(get_current_user), session: Session = Depends(get_session)):
    return session.exec(select(XPHistory).where(XPHistory.user_id == current_user.id).order_by(XPHistory.created_at.desc())).all()


@router.put("/me", response_model=UserPublic)
def update_current_user(
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    current_user: UserProfile = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Atualizar dados do usuário atual"""
    if name is not None:
        current_user.name = name
    if email is not None:
        # Validar email
        valid, msg = validate_email(email)
        if not valid:
            raise HTTPException(status_code=400, detail=msg)
        # Verificar se email já existe (exceto o dele)
        existing_email = session.exec(
            select(UserProfile).where(
                UserProfile.email.ilike(email),
                UserProfile.id != current_user.id
            )
        ).first()
        if existing_email:
            raise HTTPException(status_code=409, detail="Email já está em uso")
        current_user.email = email
    if phone is not None:
        current_user.phone = phone
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return user_to_public(current_user)


@router.delete("/me", status_code=204)
def delete_current_user(current_user: UserProfile = Depends(get_current_user), session: Session = Depends(get_session)):
    """Deletar usuário atual"""
    session.delete(current_user)
    session.commit()
    return None
