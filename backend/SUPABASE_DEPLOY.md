-- Como aplicar no Supabase manualmente (via painel web)
-- 1. Acesse https://app.supabase.com
-- 2. Selecione seu projeto
-- 3. Vá para SQL Editor (lado esquerdo)
-- 4. Clique "New query"
-- 5. Cole todo o conteúdo de schema_postgres.sql
-- 6. Clique "Run"
-- 7. Crie uma nova query e cole seed_postgres.sql
-- 8. Clique "Run"

-- Alternativa: Use psql localmente (se tiver acesso internet)
-- psql "postgresql://postgres:#DeusExiste!2025@db.libchjoccyjblobxjkeq.supabase.co:5432/postgres" -f schema_postgres.sql
-- psql "postgresql://postgres:#DeusExiste!2025@db.libchjoccyjblobxjkeq.supabase.co:5432/postgres" -f seed_postgres.sql

-- Ou use curl (execute este comando em um ambiente com internet):
-- curl -X POST https://libchjoccyjblobxjkeq.supabase.co/rest/v1/rpc/exec_sql \
--   -H "Authorization: Bearer YOUR_SERVICE_ROLE_KEY" \
--   -H "Content-Type: application/json" \
--   -d '{"sql": "...SQL HERE..."}'
