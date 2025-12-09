from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from sqlmodel import select, Session
from typing import List
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .database import init_db, get_session
from .models import UserProfile, UserPublic, UserCreate, UserLogin, Token
from .auth import hash_password, verify_password, create_access_token, get_current_user, user_to_public, SECRET_KEY, decode_token
from .routers import communities, events, users, notifications

# Ocultar documentação OpenAPI/Swagger em ambientes públicos
app = FastAPI(title="Pense Offline Backend", version="0.2.0", docs_url=None, redoc_url=None, openapi_url=None)

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080", "http://localhost:8080", "http://127.0.0.1:5173", "http://localhost:5173", "http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_templates_dir = Path(__file__).parent / "templates"


@app.on_event("startup")
def on_startup():
    """Inicializa o banco de dados ao iniciar a aplicação"""
    try:
        logger.info("=" * 60)
        logger.info("INICIANDO APLICAÇÃO PENSE OFFLINE")
        logger.info("=" * 60)
        init_db()
        logger.info("✓ Banco de dados inicializado com sucesso")
        logger.info("=" * 60)
    except Exception as e:
        logger.error("=" * 60)
        logger.error("✗ ERRO CRÍTICO AO INICIALIZAR BANCO DE DADOS")
        logger.error(f"✗ {e}")
        logger.error("=" * 60)
        raise


# Include routers ANTES de montar arquivos estáticos
app.include_router(users.router)
app.include_router(communities.router)
app.include_router(events.router)
app.include_router(notifications.router)


# Tornar a API inacessível sem token: middleware que valida presença e validade do token
# Permitimos acesso público somente a algumas rotas (root, health, login/register) e a arquivos estáticos.
PUBLIC_PATHS = ["/", "/health", "/auth/login", "/auth/register", "/users/login", "/users/register"]


@app.middleware("http")
async def require_auth_for_api(request: Request, call_next):
    path = request.url.path
    # permitir arquivos estáticos, páginas HTML e rotas públicas
    if (path.startswith("/static") or 
        path.endswith(".html") or 
        path.endswith(".js") or 
        path.endswith(".css") or 
        any(path == p or path.startswith(p + "/") for p in PUBLIC_PATHS)):
        return await call_next(request)

    auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth_header:
        return JSONResponse({"detail": "Authorization required"}, status_code=401)

    # extrair token e validar
    try:
        token = auth_header.split(" ")[1] if " " in auth_header else auth_header
        decode_token(token)
    except Exception:
        return JSONResponse({"detail": "Invalid or expired token"}, status_code=401)

    return await call_next(request)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def root():
    index_file = _templates_dir / "index.html"
    if index_file.exists():
        return index_file.read_text(encoding="utf-8")
    return "<h1>Backend online</h1><p>API de Recompensas por Redução de Tempo de Tela</p>"


# Authentication endpoints are provided in `users` router (mounted at /users)


# ===== PERFIS =====

@app.get("/profiles/ranking", response_model=List[UserPublic])
def get_ranking(session: Session = Depends(get_session), current_user: UserProfile = Depends(get_current_user)):
    """Retorna ranking de usuários por pontos"""
    users = session.exec(
        select(UserProfile).order_by(UserProfile.pontos.desc()).limit(100)
    ).all()
    return [user_to_public(u) for u in users]


@app.get("/profiles/{profile_id}", response_model=UserPublic)
def get_profile(profile_id: int, session: Session = Depends(get_session), current_user: UserProfile = Depends(get_current_user)):
    """Retorna perfil público de um usuário"""
    profile = session.get(UserProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    return user_to_public(profile)


@app.put("/profiles/me", response_model=UserPublic)
def update_my_profile(data: dict, current_user: UserProfile = Depends(get_current_user), session: Session = Depends(get_session)):
    """Atualiza perfil do usuário autenticado"""
    allowed_fields = ["name", "email", "phone"]
    for field in allowed_fields:
        if field in data and data[field] is not None:
            setattr(current_user, field, data[field])
    
    current_user.touch()
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return user_to_public(current_user)


# ===== RECOMPENSAS =====

@app.post("/rewards/add-time")
def add_screen_free_time(
    data: dict, 
    current_user: UserProfile = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    """Adiciona tempo sem tela e concede pontos (10 pontos por hora)"""
    minutos = data.get("minutos", 0)
    if minutos <= 0:
        raise HTTPException(status_code=400, detail="Minutos deve ser maior que zero")
    
    current_user.tempo_sem_tela_minutos += minutos
    pontos_ganhos = (minutos // 60) * 10  # 10 pontos por hora completa
    current_user.adicionar_pontos(pontos_ganhos)
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    
    return {
        "message": f"Você adicionou {minutos} minutos sem tela!",
        "pontos_ganhos": pontos_ganhos,
        "pontos_totais": current_user.pontos,
        "nivel": current_user.nivel
    }


@app.post("/rewards/complete-challenge")
def complete_challenge(
    data: dict,
    current_user: UserProfile = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Marca desafio como completo e concede pontos"""
    pontos = data.get("pontos", 0)
    nome_desafio = data.get("nome_desafio", "Desafio")
    
    if pontos <= 0:
        raise HTTPException(status_code=400, detail="Pontos deve ser maior que zero")
    
    current_user.desafios_completados += 1
    current_user.adicionar_pontos(pontos)
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    
    return {
        "message": f"Desafio '{nome_desafio}' completado!",
        "pontos_ganhos": pontos,
        "pontos_totais": current_user.pontos,
        "nivel": current_user.nivel,
        "desafios_completados": current_user.desafios_completados
    }


# ===== ESTATÍSTICAS =====

@app.get("/stats/global")
def get_global_stats(session: Session = Depends(get_session)):
    """Retorna estatísticas globais da plataforma"""
    total_users = session.exec(select(UserProfile)).all()
    
    if not total_users:
        return {
            "total_usuarios": 0,
            "total_pontos": 0,
            "total_tempo_sem_tela_horas": 0,
            "total_desafios": 0
        }
    
    return {
        "total_usuarios": len(total_users),
        "total_pontos": sum(u.pontos for u in total_users),
        "total_tempo_sem_tela_horas": sum(u.tempo_sem_tela_minutos for u in total_users) // 60,
        "total_desafios": sum(u.desafios_completados for u in total_users)
    }


# ===== ARQUIVOS ESTÁTICOS (SEMPRE NO FINAL) =====
# Montar arquivos estáticos APÓS todas as rotas de API

# Pasta web-files (CSS, imagens)
_static_path = Path(__file__).resolve().parents[2] / "web-files"
if _static_path.exists():
    app.mount("/web-files", StaticFiles(directory=str(_static_path)), name="web-files")

# Arquivos da raiz (HTML, JS) - SEMPRE POR ÚLTIMO
_root_path = Path(__file__).resolve().parents[2]
if _root_path.exists():
    app.mount("/", StaticFiles(directory=str(_root_path), html=True), name="root")
