"""
Script para testar o sistema de notificações
"""
import requests
import json
import random

BASE_URL = "http://127.0.0.1:8000"

def test_notification_system():
    print("=" * 60)
    print("🔔 TESTE DO SISTEMA DE NOTIFICAÇÕES")
    print("=" * 60)
    print()
    
    # 1. Criar um novo usuário
    print("1️⃣ Criando novo usuário...")
    random_num = random.randint(1000, 9999)
    user_data = {
        "username": f"teste_notif_{random_num}",
        "email": f"teste_notif_{random_num}@example.com",
        "password": "senha123",
        "name": "Teste Notificações"
    }
    
    response = requests.post(f"{BASE_URL}/users/register", json=user_data)
    
    if response.status_code == 201:
        data = response.json()
        token = data["access_token"]
        user = data["user"]
        print(f"✅ Usuário criado: {user['name']} (@{user['username']})")
        print(f"   ID: {user['id']}")
        print()
    else:
        print(f"❌ Erro ao criar usuário: {response.status_code}")
        print(f"   {response.text}")
        return
    
    # 2. Buscar notificações do usuário
    print("2️⃣ Buscando notificações...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/notifications", headers=headers)
    
    if response.status_code == 200:
        notifications = response.json()
        print(f"✅ {len(notifications)} notificação(ões) encontrada(s)")
        print()
        
        for i, notif in enumerate(notifications, 1):
            print(f"   📬 Notificação {i}:")
            print(f"      Tipo: {notif['type']}")
            print(f"      Título: {notif['title']}")
            print(f"      Mensagem: {notif['message']}")
            print(f"      Lida: {'✓' if notif['read'] else '✗'}")
            print(f"      Data: {notif['created_at']}")
            print()
    else:
        print(f"❌ Erro ao buscar notificações: {response.status_code}")
        return
    
    # 3. Contar notificações não lidas
    print("3️⃣ Contando notificações não lidas...")
    response = requests.get(f"{BASE_URL}/notifications/unread/count", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ {data['count']} notificação(ões) não lida(s)")
        print()
    
    # 4. Marcar como lida
    if notifications:
        notif_id = notifications[0]['id']
        print(f"4️⃣ Marcando notificação {notif_id} como lida...")
        response = requests.post(
            f"{BASE_URL}/notifications/{notif_id}/read",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✅ Notificação marcada como lida")
            print()
            
            # Verificar contagem novamente
            response = requests.get(f"{BASE_URL}/notifications/unread/count", headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"   Agora: {data['count']} não lida(s)")
    
    print()
    print("=" * 60)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    print()
    print("💡 Como funciona:")
    print("   • Ao criar conta, uma notificação de boas-vindas é salva no banco")
    print("   • O usuário pode consultar suas notificações via API")
    print("   • Notificações podem ser marcadas como lidas")
    print("   • Sistema conta quantas notificações não lidas existem")
    print()

if __name__ == "__main__":
    try:
        test_notification_system()
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Servidor não está rodando!")
        print("   Execute: run.ps1")
    except Exception as e:
        print(f"❌ ERRO: {e}")
