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
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@desafiopositivo.com")
FROM_NAME = os.getenv("FROM_NAME", "Desafio Positivo")

async def send_welcome_email(to_email: str, name: str, profile_id: int) -> bool:
    """
    Envia email de boas-vindas após criação de conta.
    
    Para desenvolvimento local, apenas simula o envio (retorna True).
    Para produção, configure as variáveis de ambiente SMTP.
    """
    
    # Se não houver credenciais configuradas, apenas simula o envio
    if not SMTP_USER or not SMTP_PASSWORD:
        print(f"[EMAIL SIMULADO] Para: {to_email}")
        print(f"Assunto: Bem-vindo ao Desafio Positivo, {name}!")
        print(f"Conta criada com sucesso. ID: {profile_id}")
        return True
    
    try:
        # Criar mensagem
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Bem-vindo ao Desafio Positivo, {name}!"
        message["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
        message["To"] = to_email
        
        # Corpo do email em HTML
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #007bff;">Bem-vindo ao Desafio Positivo!</h2>
                <p>Olá <strong>{name}</strong>,</p>
                <p>Sua conta foi criada com sucesso! Estamos felizes em tê-lo(a) conosco.</p>
                
                <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>ID da sua conta:</strong> {profile_id}</p>
                    <p style="margin: 5px 0;"><strong>Email:</strong> {to_email}</p>
                </div>
                
                <p>Agora você pode:</p>
                <ul>
                    <li>Editar suas informações de perfil</li>
                    <li>Participar de comunidades ativas</li>
                    <li>Registrar seu progresso</li>
                    <li>Engajar em desafios positivos</li>
                </ul>
                
                <p style="margin-top: 30px;">
                    <a href="http://127.0.0.1:8080/perfil.html?id={profile_id}" 
                       style="background: #007bff; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 4px; display: inline-block;">
                        Acessar Meu Perfil
                    </a>
                </p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                <p style="font-size: 12px; color: #666;">
                    Este é um email automático. Por favor, não responda.
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
