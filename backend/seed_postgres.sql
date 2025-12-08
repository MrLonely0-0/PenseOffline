-- Seed/example data for PenseOffline (Postgres)
-- WARNING: This file inserts password_hash values created by the local seed script.
-- You can change password_hash values or create users via the API.

BEGIN;

-- Example users (password for all is 'password' hashed with pbkdf2-sha256 in local seed)
INSERT INTO userprofile (username, email, password_hash, name, phone, pontos, nivel, xp_total)
VALUES
  ('alice', 'alice@example.com', '$pbkdf2-sha256$29000$BECIEaIUglBq7T2HMAZA6A$V2YhGi6XbpVRcltjSQ7dk7okH8fuGBlkqpLHJQwxUq4', 'Alice Silva', NULL, 20, 1, 20),
  ('bob', 'bob@example.com', '$pbkdf2-sha256$29000$BECIEaIUglBq7T2HMAZA6A$V2YhGi6XbpVRcltjSQ7dk7okH8fuGBlkqpLHJQwxUq4', 'Bob Santos', NULL, 20, 1, 20),
  ('carol', 'carol@example.com', '$pbkdf2-sha256$29000$BECIEaIUglBq7T2HMAZA6A$V2YhGi6XbpVRcltjSQ7dk7okH8fuGBlkqpLHJQwxUq4', 'Carol Lima', NULL, 0, 1, 0)
;

-- Communities
INSERT INTO community (slug, name, description, visibility, owner_id)
VALUES
  ('familia', 'Família Saudável', 'Comunidade para famílias reduzirem tempo de tela', 'public', (SELECT id FROM userprofile WHERE username='alice')),
  ('fitness', 'Fitness Offline', 'Desafios e eventos para exercícios sem tela', 'public', (SELECT id FROM userprofile WHERE username='carol'))
;

-- Memberships
INSERT INTO communitymembership (community_id, user_id, role)
VALUES
  ((SELECT id FROM community WHERE slug='familia'), (SELECT id FROM userprofile WHERE username='alice'), 'owner'),
  ((SELECT id FROM community WHERE slug='familia'), (SELECT id FROM userprofile WHERE username='bob'), 'member'),
  ((SELECT id FROM community WHERE slug='fitness'), (SELECT id FROM userprofile WHERE username='carol'), 'owner')
;

-- Events
INSERT INTO event (community_id, creator_id, title, description, xp_reward)
VALUES
  ((SELECT id FROM community WHERE slug='familia'), (SELECT id FROM userprofile WHERE username='alice'), 'Desafio Sem Tela 1', '1 hora sem telas', 20),
  ((SELECT id FROM community WHERE slug='fitness'), (SELECT id FROM userprofile WHERE username='carol'), 'Aula de Yoga Offline', '30 minutos de yoga', 15)
;

-- XP history
INSERT INTO xphistory (user_id, event_id, type, xp_amount)
VALUES
  ((SELECT id FROM userprofile WHERE username='alice'), (SELECT id FROM event WHERE title='Desafio Sem Tela 1'), 'event', 20),
  ((SELECT id FROM userprofile WHERE username='bob'), (SELECT id FROM event WHERE title='Desafio Sem Tela 1'), 'event', 20)
;

COMMIT;

-- Notes:
-- - Password hashes above were generated locally using the backend's hashing routine.
-- - If you prefer to set passwords via the API, remove password_hash values or set them to empty strings and register via /users/register.
