import os
from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session

# Carregar variáveis de ambiente do .env (se existir)
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv não está instalado, variáveis devem estar em environment

# DATABASE_URL pode ser:
#   - SQLite (dev): sqlite:///./app.db
#   - Postgres local: postgresql://user:pass@localhost:5432/dbname
#   - Supabase: postgresql://postgres:pass@db.PROJECT_ID.supabase.co:5432/postgres
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Configure connection based on DB type
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
elif "supabase" in DATABASE_URL or DATABASE_URL.startswith("postgresql"):
    # Supabase requires SSL=require; psycopg2 autodetects but we make it explicit
    connect_args = {"sslmode": "require"} if "supabase" in DATABASE_URL else {}
else:
    connect_args = {}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args, pool_pre_ping=True)


def init_db() -> None:
    # Import models to register tables
    from . import models  # noqa: F401
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
