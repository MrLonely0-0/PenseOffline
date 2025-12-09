"""
Script para testar configuração de email
Execute após configurar as credenciais SMTP no arquivo .env
"""
import sys
import os
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*80)
print("TESTE DE CONFIGURAÇÃO DE EMAIL - PENSE OFFLINE")
print("="*80)

# Carregar .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✓ Arquivo .env carregado de: {env_path}")
    else:
        print(f"⚠ Arquivo .env não encontrado em: {env_path}")
except ImportError:
    print("⚠ python-dotenv não instalado")

# Verificar configurações
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = os.getenv("SMTP_PORT", "")
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", os.getenv("SMTP_FROM", ""))

print(f"\nConfigurações encontradas:")
print(f"  SMTP_HOST: {SMTP_HOST}")
print(f"  SMTP_PORT: {SMTP_PORT}")
print(f"  SMTP_USER: {SMTP_USER}")
print(f"  SMTP_PASSWORD: {'*' * len(SMTP_PASSWORD) if SMTP_PASSWORD else '(não configurado)'}")
print(f"  FROM_EMAIL: {FROM_EMAIL}")

if not SMTP_USER or not SMTP_PASSWORD:
    print("\n" + "="*80)
    print("❌ CREDENCIAIS NÃO CONFIGURADAS")
    print("="*80)
    print("\nO sistema está em MODO SIMULAÇÃO (apenas exibe no console)")
    print("\nPara enviar emails reais:")
    print("1. Edite o arquivo: backend/.env")
    print("2. Configure as credenciais SMTP")
    print("3. Reinicie o servidor")
    print("\nVeja o guia completo em: backend/CONFIGURAR_EMAIL.md")
    print("="*80 + "\n")
    sys.exit(0)

# Tentar enviar email de teste
print("\n" + "="*80)
print("TESTANDO ENVIO DE EMAIL...")
print("="*80)

import asyncio
from app.email_service import send_welcome_email

async def test_email():
    email_destino = input("\nDigite o email de destino para teste: ").strip()
    if not email_destino:
        print("❌ Email inválido")
        return
    
    print(f"\nEnviando email de teste para: {email_destino}")
    print("Aguarde...")
    
    try:
        resultado = await send_welcome_email(
            to_email=email_destino,
            name="Usuário Teste",
            profile_id=999
        )
        
        if resultado:
            print("\n✓ EMAIL ENVIADO COM SUCESSO!")
            print(f"✓ Verifique a caixa de entrada de: {email_destino}")
            print("✓ Não se esqueça de verificar a pasta de SPAM")
        else:
            print("\n❌ Falha ao enviar email")
            print("Verifique os logs acima para mais detalhes")
    
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test_email())

print("\n" + "="*80)
print("TESTE CONCLUÍDO")
print("="*80 + "\n")
