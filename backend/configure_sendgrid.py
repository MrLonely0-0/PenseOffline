"""
Script para configurar SendGrid rapidamente
Executa após obter a API Key do SendGrid
"""
import os
from pathlib import Path

def configure_sendgrid():
    print("=" * 60)
    print("🚀 CONFIGURAÇÃO RÁPIDA - SENDGRID")
    print("=" * 60)
    print()
    
    # Pedir API Key
    print("📋 Cole sua API Key do SendGrid")
    print("   (formato: SG.xxxxxxxxxxxxxxxxxxxxxxxxx)")
    print()
    api_key = input("API Key: ").strip()
    
    if not api_key.startswith("SG."):
        print()
        print("❌ ERRO: API Key deve começar com 'SG.'")
        print("   Verifique se copiou corretamente")
        return
    
    # Pedir email do remetente
    print()
    print("📧 Qual email você verificou no SendGrid?")
    print("   (ex: noreply@penseoffline.com)")
    print()
    from_email = input("Email remetente: ").strip()
    
    if "@" not in from_email:
        print()
        print("❌ ERRO: Email inválido")
        return
    
    # Atualizar .env
    env_path = Path(__file__).parent / ".env"
    
    if not env_path.exists():
        print()
        print("❌ ERRO: Arquivo .env não encontrado")
        return
    
    print()
    print("📝 Atualizando arquivo .env...")
    
    # Ler conteúdo atual
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Atualizar linhas de email
    new_lines = []
    updated = {
        "SMTP_HOST": False,
        "SMTP_PORT": False,
        "SMTP_USER": False,
        "SMTP_PASSWORD": False,
        "FROM_EMAIL": False,
        "FROM_NAME": False
    }
    
    for line in lines:
        if line.startswith("SMTP_HOST="):
            new_lines.append("SMTP_HOST=smtp.sendgrid.net\n")
            updated["SMTP_HOST"] = True
        elif line.startswith("SMTP_PORT="):
            new_lines.append("SMTP_PORT=587\n")
            updated["SMTP_PORT"] = True
        elif line.startswith("SMTP_USER="):
            new_lines.append("SMTP_USER=apikey\n")
            updated["SMTP_USER"] = True
        elif line.startswith("SMTP_PASSWORD="):
            new_lines.append(f"SMTP_PASSWORD={api_key}\n")
            updated["SMTP_PASSWORD"] = True
        elif line.startswith("FROM_EMAIL="):
            new_lines.append(f"FROM_EMAIL={from_email}\n")
            updated["FROM_EMAIL"] = True
        elif line.startswith("FROM_NAME="):
            new_lines.append("FROM_NAME=Pense Offline\n")
            updated["FROM_NAME"] = True
        else:
            new_lines.append(line)
    
    # Escrever de volta
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    print()
    print("✅ Configuração concluída!")
    print()
    print("📊 Variáveis configuradas:")
    print(f"   • SMTP_HOST: smtp.sendgrid.net")
    print(f"   • SMTP_PORT: 587")
    print(f"   • SMTP_USER: apikey")
    print(f"   • SMTP_PASSWORD: {api_key[:10]}...{api_key[-4:]}")
    print(f"   • FROM_EMAIL: {from_email}")
    print(f"   • FROM_NAME: Pense Offline")
    print()
    print("🧪 Próximo passo:")
    print("   Execute: python test_email.py")
    print("   Para testar o envio de email")
    print()

if __name__ == "__main__":
    try:
        configure_sendgrid()
    except KeyboardInterrupt:
        print()
        print("❌ Configuração cancelada")
    except Exception as e:
        print()
        print(f"❌ ERRO: {e}")
