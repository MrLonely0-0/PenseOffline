"""
Script para redefinir senha de usuário
"""
from sqlmodel import Session, select, create_engine
from app.models import UserProfile
from app.database import DATABASE_URL
from app.auth import hash_password

def reset_password():
    print("=" * 60)
    print("🔑 REDEFINIR SENHA DE USUÁRIO")
    print("=" * 60)
    print()
    
    username = input("Digite o username: ").strip()
    new_password = input("Digite a nova senha: ").strip()
    
    if not username or not new_password:
        print("❌ Username e senha são obrigatórios!")
        return
    
    print()
    print(f"Conectando ao banco de dados...")
    
    engine = create_engine(DATABASE_URL)
    session = Session(engine)
    
    # Buscar usuário
    user = session.exec(
        select(UserProfile).where(UserProfile.username.ilike(username))
    ).first()
    
    if not user:
        print(f"❌ Usuário '{username}' não encontrado!")
        session.close()
        return
    
    # Atualizar senha
    user.password_hash = hash_password(new_password)
    session.add(user)
    session.commit()
    
    print()
    print("✅ Senha atualizada com sucesso!")
    print()
    print(f"   Usuário: {user.username}")
    print(f"   Nome: {user.name}")
    print(f"   Email: {user.email}")
    print(f"   Nova senha: {new_password}")
    print()
    print("Agora você pode fazer login com a nova senha.")
    
    session.close()

if __name__ == "__main__":
    try:
        reset_password()
    except KeyboardInterrupt:
        print("\n❌ Operação cancelada")
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
