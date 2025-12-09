from sqlmodel import Session, select, create_engine
from app.models import UserProfile
from app.database import DATABASE_URL
from app.auth import hash_password

engine = create_engine(DATABASE_URL)
session = Session(engine)

user = session.exec(select(UserProfile).where(UserProfile.username == "danielpereira")).first()

if user:
    user.password_hash = hash_password("senha123")
    session.add(user)
    session.commit()
    print(f"✅ Senha do usuário '{user.username}' atualizada para: senha123")
else:
    print("❌ Usuário não encontrado")

session.close()
