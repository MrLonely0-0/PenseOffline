#!/bin/bash
# Script de inicialização para Render
# Este script é executado antes de iniciar a aplicação

echo "🚀 Iniciando configuração do ambiente..."

# Verificar se DATABASE_URL está definida
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  DATABASE_URL não definida. Usando SQLite local."
    export DATABASE_URL="sqlite:///./app.db"
fi

echo "✅ Variáveis de ambiente configuradas"

# Aplicar migrações do banco de dados (se houver)
echo "🔄 Aplicando migrações do banco de dados..."
python -c "from app.database import init_db; init_db()"

echo "✅ Banco de dados inicializado"

# Popular banco com dados iniciais (se necessário)
if [ "$SEED_DATABASE" = "true" ]; then
    echo "🌱 Populando banco de dados com dados iniciais..."
    python seed.py
    echo "✅ Dados iniciais inseridos"
fi

echo "🎉 Configuração concluída! Iniciando aplicação..."

# Iniciar a aplicação
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
