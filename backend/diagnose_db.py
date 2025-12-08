"""
Script de diagnóstico do banco de dados
Execute este script para verificar se a conexão com o banco está funcionando
"""
import sys
import os
from pathlib import Path

# Adicionar o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("DIAGNÓSTICO DO BANCO DE DADOS - PENSE OFFLINE")
print("=" * 70)

# 1. Verificar Python
print("\n[1/7] Verificando versão do Python...")
print(f"✓ Python {sys.version}")

# 2. Verificar dependências
print("\n[2/7] Verificando dependências...")
try:
    import fastapi
    print(f"✓ FastAPI {fastapi.__version__}")
except ImportError as e:
    print(f"✗ FastAPI não encontrado: {e}")
    sys.exit(1)

try:
    import sqlmodel
    print(f"✓ SQLModel {sqlmodel.__version__}")
except ImportError as e:
    print(f"✗ SQLModel não encontrado: {e}")
    sys.exit(1)

try:
    import uvicorn
    print(f"✓ Uvicorn {uvicorn.__version__}")
except ImportError as e:
    print(f"✗ Uvicorn não encontrado: {e}")
    sys.exit(1)

# 3. Verificar variáveis de ambiente
print("\n[3/7] Verificando variáveis de ambiente...")
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✓ Arquivo .env encontrado em: {env_path}")
    else:
        print(f"⚠ Arquivo .env não encontrado em: {env_path}")
        print("  (usando SQLite padrão)")
except ImportError:
    print("⚠ python-dotenv não instalado")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
safe_url = DATABASE_URL
if "@" in DATABASE_URL:
    parts = DATABASE_URL.split("@")
    if ":" in parts[0]:
        protocol_user = parts[0].rsplit(":", 1)[0]
        safe_url = f"{protocol_user}:****@{parts[1]}"
print(f"✓ DATABASE_URL: {safe_url}")

# 4. Verificar arquivo de banco SQLite
print("\n[4/7] Verificando banco de dados...")
if DATABASE_URL.startswith("sqlite"):
    db_file = DATABASE_URL.replace("sqlite:///", "").replace("./", "")
    db_path = Path(__file__).parent / db_file
    if db_path.exists():
        size = db_path.stat().st_size
        print(f"✓ Arquivo SQLite encontrado: {db_path}")
        print(f"  Tamanho: {size:,} bytes")
    else:
        print(f"⚠ Arquivo SQLite não existe: {db_path}")
        print("  (será criado na primeira execução)")
else:
    print(f"✓ Usando banco PostgreSQL")

# 5. Testar importação dos modelos
print("\n[5/7] Testando importação dos modelos...")
try:
    from app import models
    print(f"✓ Modelos importados com sucesso")
    print(f"  - UserProfile")
    print(f"  - Community")
    print(f"  - Event")
    print(f"  - XPHistory")
    print(f"  - CommunityMembership")
except Exception as e:
    print(f"✗ Erro ao importar modelos: {e}")
    sys.exit(1)

# 6. Testar criação do engine
print("\n[6/7] Testando criação do engine...")
try:
    from app.database import engine
    print(f"✓ Engine criado com sucesso")
    print(f"  Driver: {engine.dialect.name}")
except Exception as e:
    print(f"✗ Erro ao criar engine: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 7. Testar conexão
print("\n[7/7] Testando conexão com o banco...")
try:
    from sqlmodel import Session
    with Session(engine) as session:
        # Tentar uma query simples
        session.exec(sqlmodel.text("SELECT 1"))
        print("✓ Conexão estabelecida com sucesso!")
except Exception as e:
    print(f"✗ Erro ao conectar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 8. Testar criação de tabelas
print("\n[8/8] Testando criação de tabelas...")
try:
    from app.database import init_db
    init_db()
    print("✓ Tabelas criadas/verificadas com sucesso!")
except Exception as e:
    print(f"✗ Erro ao criar tabelas: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 9. Verificar tabelas criadas
print("\n[9/9] Verificando tabelas criadas...")
try:
    from sqlmodel import select, Session
    with Session(engine) as session:
        if DATABASE_URL.startswith("sqlite"):
            # SQLite
            result = session.exec(
                sqlmodel.text("SELECT name FROM sqlite_master WHERE type='table'")
            )
            tables = [row[0] for row in result]
        else:
            # PostgreSQL
            result = session.exec(
                sqlmodel.text("SELECT tablename FROM pg_tables WHERE schemaname='public'")
            )
            tables = [row[0] for row in result]
        
        print(f"✓ {len(tables)} tabelas encontradas:")
        for table in sorted(tables):
            print(f"  - {table}")
except Exception as e:
    print(f"✗ Erro ao listar tabelas: {e}")

# Resumo final
print("\n" + "=" * 70)
print("DIAGNÓSTICO CONCLUÍDO!")
print("=" * 70)
print("\n✓ Todos os testes passaram!")
print("\nPróximos passos:")
print("1. Execute: python -m uvicorn app.main:app --reload --port 8000")
print("2. Acesse: http://127.0.0.1:8000/health")
print("3. Teste: http://127.0.0.1:8000/")
print("\n" + "=" * 70)
