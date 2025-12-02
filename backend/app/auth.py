from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select

from .models import UserProfile, UserPublic
from .database import get_session

import os

# Configuração de segurança
SECRET_KEY = os.getenv("SECRET_KEY", "seu-secret-key-super-seguro-mude-em-producao-12345")  # MUDAR EM PRODUÇÃO
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))  # 24 horas por padrão

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")
security = HTTPBearer()


def hash_password(password: str) -> str:
    """Gera hash da senha (trunca em 72 bytes se necessário devido a limitação do bcrypt)"""
    # Bcrypt tem limite de 72 bytes - truncar se necessário
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se senha corresponde ao hash (trunca em 72 bytes se necessário)"""
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        plain_password = password_bytes[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """Decodifica token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> UserProfile:
    """Obtém usuário atual a partir do token"""
    token = credentials.credentials
    payload = decode_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )
    
    user = session.exec(select(UserProfile).where(UserProfile.username == username)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
        )
    
    # Atualizar último acesso
    user.ultimo_acesso = datetime.utcnow()
    session.add(user)
    session.commit()
    
    return user


def user_to_public(user: UserProfile) -> UserPublic:
    """Converte UserProfile para UserPublic (sem senha)"""
    return UserPublic(
        id=user.id,
        username=user.username,
        name=user.name,
        email=user.email,
        pontos=user.pontos,
        xp_total=user.xp_total,
        nivel=user.nivel,
        tempo_sem_tela_minutos=user.tempo_sem_tela_minutos,
        desafios_completados=user.desafios_completados,
        dias_consecutivos=user.dias_consecutivos,
        created_at=user.created_at
    )
