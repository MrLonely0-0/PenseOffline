from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from typing import List
import json


class CommunityMembership(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    community_id: int = Field(foreign_key="community.id")
    user_id: int = Field(foreign_key="userprofile.id")
    role: str = Field(default="member")
    joined_at: datetime = Field(default_factory=datetime.utcnow)


class Community(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    name: str
    description: Optional[str] = None
    visibility: str = Field(default="public")
    owner_id: Optional[int] = Field(default=None, foreign_key="userprofile.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    community_id: Optional[int] = Field(default=None, foreign_key="community.id")
    creator_id: int = Field(foreign_key="userprofile.id")
    title: str
    description: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    xp_reward: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class XPHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="userprofile.id")
    event_id: Optional[int] = Field(default=None, foreign_key="event.id")
    type: str = Field(default="manual")
    xp_amount: int = Field(default=0)
    metadata: Optional[dict] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    name: str
    phone: Optional[str] = None

    pontos: int = Field(default=0)
    nivel: int = Field(default=1)
    xp_total: int = Field(default=0)
    tempo_sem_tela_minutos: int = Field(default=0)
    desafios_completados: int = Field(default=0)
    dias_consecutivos: int = Field(default=0)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    ultimo_acesso: Optional[datetime] = None

    # relationships handled via explicit queries to keep models simple and avoid mapper issues

    def touch(self):
        self.updated_at = datetime.utcnow()

    def adicionar_pontos(self, pontos: int):
        self.pontos += pontos
        self.xp_total += pontos
        # A cada 100 pontos, sobe um nível
        self.nivel = (self.pontos // 100) + 1
        self.touch()


class UserPublic(SQLModel):
    id: int
    username: str
    name: str
    email: str
    pontos: int
    nivel: int
    xp_total: int
    tempo_sem_tela_minutos: int
    desafios_completados: int
    dias_consecutivos: int
    created_at: datetime


class UserCreate(SQLModel):
    username: str
    email: str
    password: str
    name: str
    phone: Optional[str] = None


class UserLogin(SQLModel):
    username: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str
    user: UserPublic
