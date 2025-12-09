import psycopg2

conn = psycopg2.connect('postgresql://postgres:#DeusExiste!2025@db.libchjoccyjblobxjkeq.supabase.co:5432/postgres')
cur = conn.cursor()

# Buscar usuários
cur.execute('SELECT id, username, email, name, pontos, nivel, created_at FROM userprofile ORDER BY id DESC LIMIT 5')
rows = cur.fetchall()

print('\n' + '='*80)
print('USUÁRIOS NO SUPABASE')
print('='*80)

if rows:
    for row in rows:
        print(f'\n✓ ID: {row[0]}')
        print(f'  Username: {row[1]}')
        print(f'  Email: {row[2]}')
        print(f'  Nome: {row[3]}')
        print(f'  Pontos: {row[4]} | Nível: {row[5]}')
        print(f'  Criado em: {row[6]}')
else:
    print('\nNenhum usuário encontrado')

# Contar total
cur.execute('SELECT COUNT(*) FROM userprofile')
total = cur.fetchone()[0]
print(f'\n✓ Total de usuários no banco: {total}')
print('='*80 + '\n')

conn.close()
