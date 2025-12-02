from .database import init_db, engine
from .models import UserProfile
from sqlmodel import Session

SAMPLE = [
    {"name": "Alice", "email": "alice@example.com", "phone": "+55 11 90000-0001"},
    {"name": "Bruno", "email": "bruno@example.com", "phone": "+55 11 90000-0002"},
    {"name": "Carla", "email": "carla@example.com", "phone": "+55 11 90000-0003"},
]

def run():
    init_db()
    with Session(engine) as session:
        existing = session.query(UserProfile).count()
        if existing:
            print(f"Database already has {existing} profiles; skipping seed.")
            return
        for item in SAMPLE:
            session.add(UserProfile(**item))
        session.commit()
        print("Seed complete: added", len(SAMPLE), "profiles")

if __name__ == "__main__":
    run()
