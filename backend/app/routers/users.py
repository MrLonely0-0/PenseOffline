from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlmodel import Session, select
from typing import List, Optional
import re
import logging

from ..database import get_session
from ..models import UserProfile, UserPublic, UserCreate, UserLogin, Token, XPHistory, Notification
from ..auth import get_current_user, hash_password, verify_password, create_access_token, user_to_public

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)


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
    logger.info("=" * 70)
    logger.info("📝 NOVA REQUISIÇÃO DE CADASTRO")
    logger.info("=" * 70)
    logger.info(f"👤 Username: {user_data.username}")
    logger.info(f"📧 Email: {user_data.email}")
    logger.info(f"📛 Nome: {user_data.name}")
    logger.info(f"📱 Telefone: {user_data.phone or 'Não fornecido'}")
    
    # Validar username (como @instagram)
    logger.info("🔍 Validando username...")
    valid, msg = validate_username(user_data.username)
    if not valid:
        logger.warning(f"❌ Validação username falhou: {msg}")
        raise HTTPException(status_code=400, detail=msg)
    logger.info("✅ Username válido")
    
    # Validar email
    logger.info("🔍 Validando email...")
    valid, msg = validate_email(user_data.email)
    if not valid:
        logger.warning(f"❌ Validação email falhou: {msg}")
        raise HTTPException(status_code=400, detail=msg)
    logger.info("✅ Email válido")
    
    # Verificar username único (case-insensitive)
    logger.info("🔍 Verificando se username já existe...")
    existing_user = session.exec(
        select(UserProfile).where(UserProfile.username.ilike(user_data.username))
    ).first()
    if existing_user:
        logger.warning(f"❌ Username '{user_data.username}' já existe (ID: {existing_user.id})")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '@{user_data.username}' já está em uso"
        )
    logger.info("✅ Username disponível")
    
    # Verificar email único (case-insensitive)
    logger.info("🔍 Verificando se email já existe...")
    existing_email = session.exec(
        select(UserProfile).where(UserProfile.email.ilike(user_data.email))
    ).first()
    if existing_email:
        logger.warning(f"❌ Email '{user_data.email}' já cadastrado (ID: {existing_email.id})")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já está cadastrado"
        )
    logger.info("✅ Email disponível")
    
    # Criar novo usuário
    logger.info("💾 Criando usuário no banco de dados...")
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
    logger.info(f"✅ Usuário criado com sucesso! ID: {user.id}")
    
    # Registrar notificação de boas-vindas no banco
    logger.info("🔔 Criando notificação de boas-vindas...")
    notification = Notification(
        user_id=user.id,
        type="welcome",
        title="Bem-vindo ao Pense Offline!",
        message=f"Olá {user.name}! Obrigado por criar sua conta. Estamos felizes em ter você conosco!"
    )
    session.add(notification)
    session.commit()
    logger.info(f"✅ Notificação criada! ID: {notification.id}")
    
    logger.info("🔑 Gerando token de autenticação...")
    token = create_access_token({"sub": user.username})
    logger.info("✅ Token gerado com sucesso")
    
    logger.info("=" * 70)
    logger.info("🎉 CADASTRO CONCLUÍDO COM SUCESSO!")
    logger.info(f"   Usuário: {user.username} (ID: {user.id})")
    logger.info(f"   Email: {user.email}")
    logger.info("=" * 70)
    
    return Token(access_token=token, token_type="bearer", user=user_to_public(user))




@router.post("/login", response_model=Token)
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    logger.info("=" * 70)
    logger.info("🔐 NOVA REQUISIÇÃO DE LOGIN")
    logger.info("=" * 70)
    logger.info(f"👤 Username: {credentials.username}")
    
    logger.info("🔍 Buscando usuário no banco...")
    user = session.exec(select(UserProfile).where(UserProfile.username.ilike(credentials.username))).first()
    
    if not user:
        logger.warning(f"❌ Usuário '{credentials.username}' não encontrado")
        raise HTTPException(status_code=401, detail="Username ou senha incorretos")
    
    logger.info(f"✅ Usuário encontrado: {user.username} (ID: {user.id})")
    logger.info("🔍 Verificando senha...")
    
    if not verify_password(credentials.password, user.password_hash):
        logger.warning(f"❌ Senha incorreta para usuário '{credentials.username}'")
        raise HTTPException(status_code=401, detail="Username ou senha incorretos")
    
    logger.info("✅ Senha correta")
    logger.info("📅 Atualizando último acesso...")
    
    from datetime import datetime
    user.ultimo_acesso = datetime.utcnow()
    session.add(user)
    session.commit()
    logger.info(f"✅ Último acesso atualizado: {user.ultimo_acesso}")
    
    logger.info("🔑 Gerando token de autenticação...")
    token = create_access_token({"sub": user.username})
    logger.info("✅ Token gerado")
    
    logger.info("=" * 70)
    logger.info("🎉 LOGIN REALIZADO COM SUCESSO!")
    logger.info(f"   Usuário: {user.username} (ID: {user.id})")
    logger.info(f"   Nome: {user.name}")
    logger.info("=" * 70)
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
