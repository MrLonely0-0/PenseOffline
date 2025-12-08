from sqlmodel import Session
from app.database import engine, init_db
from app.models import UserProfile, Community, CommunityMembership, Event, XPHistory
from app.auth import hash_password


def seed():
    init_db()
    with Session(engine) as session:
        # Usuários de exemplo
        alice = UserProfile(username="alice", name="Alice Silva", email="alice@example.com", password_hash=hash_password("password"))
        bob = UserProfile(username="bob", name="Bob Santos", email="bob@example.com", password_hash=hash_password("password"))
        carol = UserProfile(username="carol", name="Carol Lima", email="carol@example.com", password_hash=hash_password("password"))

        session.add_all([alice, bob, carol])
        session.commit()
        session.refresh(alice)
        session.refresh(bob)
        session.refresh(carol)

        # Comunidades
        comm1 = Community(slug="familia", name="Família Saudável", description="Comunidade para famílias reduzirem tempo de tela")
        comm2 = Community(slug="fitness", name="Fitness Offline", description="Desafios e eventos para exercícios sem tela")
        session.add_all([comm1, comm2])
        session.commit()
        session.refresh(comm1)
        session.refresh(comm2)

        # Memberships
        m1 = CommunityMembership(community_id=comm1.id, user_id=alice.id, role="owner")
        m2 = CommunityMembership(community_id=comm1.id, user_id=bob.id)
        m3 = CommunityMembership(community_id=comm2.id, user_id=carol.id, role="owner")
        session.add_all([m1, m2, m3])

        # Eventos
        e1 = Event(community_id=comm1.id, creator_id=alice.id, title="Desafio Sem Tela 1", description="1 hora sem telas", xp_reward=20)
        e2 = Event(community_id=comm2.id, creator_id=carol.id, title="Aula de Yoga Offline", description="30 minutos de yoga", xp_reward=15)
        session.add_all([e1, e2])
        session.commit()
        session.refresh(e1)
        session.refresh(e2)

        # Histórico de XP
        hx1 = XPHistory(user_id=alice.id, event_id=e1.id, type="event", xp_amount=20)
        hx2 = XPHistory(user_id=bob.id, event_id=e1.id, type="event", xp_amount=20)
        session.add_all([hx1, hx2])

        # Atualizar pontos/xp totals
        alice.adicionar_pontos(20)
        bob.adicionar_pontos(20)

        session.commit()

    print("Seed completed.")


if __name__ == "__main__":
    seed()
from app.database import init_db, engine
from app.models import UserProfile, Community, Event
from sqlmodel import Session, select


def run_seed():
    init_db()
    with Session(engine) as session:
        # Create sample users
        if not session.exec(select(UserProfile)).first():
            u1 = UserProfile(username="alice", email="alice@example.com", password_hash="", name="Alice")
            u2 = UserProfile(username="bob", email="bob@example.com", password_hash="", name="Bob")
            session.add(u1)
            session.add(u2)
            session.commit()
        # Create sample community
        if not session.exec(select(Community)).first():
            c = Community(slug="comunidade-geral", name="Comunidade Geral", description="Comunidade principal")
            session.add(c)
            session.commit()
        # Create sample event
        if not session.exec(select(Event)).first():
            e = Event(title="Primeiro Evento", description="Evento de teste", creator_id=1, xp_reward=20)
            session.add(e)
            session.commit()


if __name__ == "__main__":
    run_seed()
