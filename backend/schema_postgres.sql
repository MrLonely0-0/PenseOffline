-- PostgreSQL schema for PenseOffline
-- Run with: psql <connection_string> -f schema_postgres.sql

-- Users table
CREATE TABLE IF NOT EXISTS userprofile (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(320) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    name VARCHAR(200) NOT NULL,
    phone VARCHAR(50),
    pontos INTEGER NOT NULL DEFAULT 0,
    nivel INTEGER NOT NULL DEFAULT 1,
    xp_total INTEGER NOT NULL DEFAULT 0,
    tempo_sem_tela_minutos INTEGER NOT NULL DEFAULT 0,
    desafios_completados INTEGER NOT NULL DEFAULT 0,
    dias_consecutivos INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    ultimo_acesso TIMESTAMP WITH TIME ZONE
);

-- Communities
CREATE TABLE IF NOT EXISTS community (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(150) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    visibility VARCHAR(20) NOT NULL DEFAULT 'public',
    owner_id INTEGER REFERENCES userprofile(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Community memberships
CREATE TABLE IF NOT EXISTS communitymembership (
    id SERIAL PRIMARY KEY,
    community_id INTEGER NOT NULL REFERENCES community(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES userprofile(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL DEFAULT 'member',
    joined_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    CONSTRAINT unique_membership UNIQUE (community_id, user_id)
);

-- Events
CREATE TABLE IF NOT EXISTS event (
    id SERIAL PRIMARY KEY,
    community_id INTEGER REFERENCES community(id) ON DELETE SET NULL,
    creator_id INTEGER REFERENCES userprofile(id) ON DELETE SET NULL,
    title VARCHAR(300) NOT NULL,
    description TEXT,
    starts_at TIMESTAMP WITH TIME ZONE,
    ends_at TIMESTAMP WITH TIME ZONE,
    xp_reward INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- XP history
CREATE TABLE IF NOT EXISTS xphistory (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES userprofile(id) ON DELETE CASCADE,
    event_id INTEGER REFERENCES event(id) ON DELETE SET NULL,
    type VARCHAR(50) NOT NULL DEFAULT 'manual',
    xp_amount INTEGER NOT NULL DEFAULT 0,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Useful indexes (uniques above already create indexes)
CREATE INDEX IF NOT EXISTS idx_userprofile_username ON userprofile(username);
CREATE INDEX IF NOT EXISTS idx_userprofile_email ON userprofile(email);
CREATE INDEX IF NOT EXISTS idx_community_slug ON community(slug);
