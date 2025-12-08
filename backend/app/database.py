import os
from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente do .env (se existir)
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        logger.info(f"Arquivo .env carregado de: {env_path}")
    else:
        logger.warning(f"Arquivo .env não encontrado em: {env_path}")
except ImportError:
    logger.warning("python-dotenv não instalado, usando variáveis de ambiente do sistema")

# DATABASE_URL pode ser:
#   - SQLite (dev): sqlite:///./app.db
#   - Postgres local: postgresql://user:pass@localhost:5432/dbname
#   - Supabase: postgresql://postgres:pass@db.PROJECT_ID.supabase.co:5432/postgres
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Mascarar senha no log
safe_url = DATABASE_URL
if "@" in DATABASE_URL:
    parts = DATABASE_URL.split("@")
    if ":" in parts[0]:
        protocol_user = parts[0].rsplit(":", 1)[0]
        safe_url = f"{protocol_user}:****@{parts[1]}"

logger.info(f"Conectando ao banco de dados: {safe_url}")

# Configure connection based on DB type
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    logger.info("Usando SQLite - modo de desenvolvimento")
elif "supabase" in DATABASE_URL or DATABASE_URL.startswith("postgresql"):
    # Supabase requires SSL=require; psycopg2 autodetects but we make it explicit
    connect_args = {"sslmode": "require"} if "supabase" in DATABASE_URL else {}
    logger.info(f"Usando PostgreSQL - SSL: {'require' if 'supabase' in DATABASE_URL else 'prefer'}")
else:
    connect_args = {}
    logger.warning(f"Tipo de banco desconhecido para URL: {safe_url}")

try:
    engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args, pool_pre_ping=True)
    logger.info("Engine do banco de dados criado com sucesso")
except Exception as e:
    logger.error(f"Erro ao criar engine do banco de dados: {e}")
    raise


def init_db() -> None:
    """Inicializa o banco de dados criando todas as tabelas"""
    try:
        logger.info("Iniciando criação de tabelas...")
        # Import models to register tables
        from . import models  # noqa: F401
        SQLModel.metadata.create_all(engine)
        logger.info("✓ Tabelas criadas com sucesso!")
    except Exception as e:
        logger.error(f"✗ Erro ao criar tabelas: {e}")
        raise


def get_session():
    """Retorna uma sessão do banco de dados"""
    with Session(engine) as session:
        yield session
