import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from typing import Optional

# Configurações de email (variáveis de ambiente ou valores padrão para desenvolvimento)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", os.getenv("SMTP_FROM", "noreply@penseoffline.com"))
FROM_NAME = os.getenv("FROM_NAME", "Pense Offline")

async def send_welcome_email(to_email: str, name: str, profile_id: int) -> bool:
    """
    Envia email de boas-vindas após criação de conta.
    
    Para desenvolvimento local, apenas simula o envio (retorna True).
    Para produção, configure as variáveis de ambiente SMTP.
    """
    
    # Se não houver credenciais configuradas, apenas simula o envio
    if not SMTP_USER or not SMTP_PASSWORD:
        print(f"\n{'='*80}")
        print(f"📧 EMAIL DE BOAS-VINDAS")
        print(f"{'='*80}")
        print(f"Para: {to_email}")
        print(f"Nome: {name}")
        print(f"ID da Conta: {profile_id}")
        print(f"\n✓ Seja bem-vindo(a), {name}!")
        print(f"✓ Obrigado por criar sua conta no Pense Offline!")
        print(f"✓ Sua jornada para uma vida mais equilibrada começa agora.")
        print(f"{'='*80}\n")
        return True
    
    try:
        # Criar mensagem
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Seja bem-vindo(a) ao Pense Offline, {name}!"
        message["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
        message["To"] = to_email
        
        # Corpo do email em HTML
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #007bff;">🎉 Seja bem-vindo(a) ao Pense Offline!</h2>
                <p>Olá <strong>{name}</strong>,</p>
                <p><strong>Obrigado por criar sua conta!</strong></p>
                <p>Estamos muito felizes em tê-lo(a) conosco nesta jornada para uma vida mais equilibrada e consciente.</p>
                
                <div style="background: #f0f8ff; padding: 20px; border-left: 4px solid #007bff; margin: 20px 0;">
                    <p style="margin: 0; font-size: 16px;">
                        ✓ Sua conta foi criada com sucesso!<br>
                        ✓ Você já pode começar a usar o Pense Offline<br>
                        ✓ Comece sua jornada rumo a uma vida mais presente
                    </p>
                </div>
                
                <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>ID da sua conta:</strong> {profile_id}</p>
                    <p style="margin: 5px 0;"><strong>Email:</strong> {to_email}</p>
                </div>
                
                <p>Agora você pode:</p>
                <ul>
                    <li>✓ Registrar seu tempo longe das telas</li>
                    <li>✓ Completar desafios e ganhar pontos</li>
                    <li>✓ Participar de comunidades</li>
                    <li>✓ Acompanhar seu progresso e evolução</li>
                    <li>✓ Competir no ranking com outros usuários</li>
                </ul>
                
                <p style="margin-top: 30px;">
                    <a href="http://127.0.0.1:8080/dashboard.html" 
                       style="background: #007bff; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 4px; display: inline-block;">
                        Começar Agora
                    </a>
                </p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                <p style="font-size: 12px; color: #666;">
                    Este é um email automático do Pense Offline. Por favor, não responda.
                </p>
            </div>
        </body>
        </html>
        """
        
        # Anexar HTML
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Enviar email
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
        )
        
        print(f"Email enviado com sucesso para {to_email}")
        return True
        
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        # Não falha a criação da conta se o email falhar
        return False
