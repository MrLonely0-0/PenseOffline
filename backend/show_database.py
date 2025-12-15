#!/usr/bin/env python3
"""
Script de demonstração visual que mostra o banco de dados funcionando.
Exibe informações sobre usuários, comunidades, eventos e estatísticas.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sqlmodel import Session, select
from app.database import engine, init_db, DATABASE_URL
from app.models import UserProfile, Community, Event, XPHistory, CommunityMembership
from datetime import datetime


def print_header(title: str):
    """Imprime um cabeçalho formatado"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_section(title: str):
    """Imprime uma seção formatada"""
    print(f"\n{'─' * 80}")
    print(f"  📊 {title}")
    print(f"{'─' * 80}\n")


def display_database_info():
    """Exibe informações sobre o banco de dados"""
    print_header("🗄️  DEMONSTRAÇÃO DO BANCO DE DADOS - PenseOffline")
    
    print(f"\n🔗 Banco de dados conectado: {DATABASE_URL}")
    print(f"⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    with Session(engine) as session:
        # Contar registros
        user_count = len(session.exec(select(UserProfile)).all())
        community_count = len(session.exec(select(Community)).all())
        event_count = len(session.exec(select(Event)).all())
        xp_count = len(session.exec(select(XPHistory)).all())
        membership_count = len(session.exec(select(CommunityMembership)).all())
        
        print("\n📈 Estatísticas Gerais:")
        print(f"  • Usuários: {user_count}")
        print(f"  • Comunidades: {community_count}")
        print(f"  • Eventos: {event_count}")
        print(f"  • Registros de XP: {xp_count}")
        print(f"  • Memberships: {membership_count}")
        
        # Listar usuários
        if user_count > 0:
            print_section("👥 Usuários Cadastrados")
            users = session.exec(select(UserProfile).order_by(UserProfile.pontos.desc())).all()
            
            print(f"{'ID':<5} {'Username':<20} {'Nome':<25} {'Pontos':<10} {'Nível':<8} {'XP Total':<10}")
            print("─" * 80)
            for user in users:
                print(f"{user.id:<5} {user.username:<20} {user.name:<25} {user.pontos:<10} {user.nivel:<8} {user.xp_total:<10}")
        
        # Listar comunidades
        if community_count > 0:
            print_section("🏘️  Comunidades")
            communities = session.exec(select(Community)).all()
            
            print(f"{'ID':<5} {'Slug':<25} {'Nome':<35} {'Membros':<10}")
            print("─" * 80)
            for comm in communities:
                member_count = len(session.exec(
                    select(CommunityMembership).where(CommunityMembership.community_id == comm.id)
                ).all())
                print(f"{comm.id:<5} {comm.slug:<25} {comm.name:<35} {member_count:<10}")
                if comm.description:
                    print(f"      └─ {comm.description}")
        
        # Listar eventos
        if event_count > 0:
            print_section("📅 Eventos")
            events = session.exec(select(Event)).all()
            
            print(f"{'ID':<5} {'Título':<40} {'Recompensa XP':<15} {'Criador ID':<12}")
            print("─" * 80)
            for event in events:
                print(f"{event.id:<5} {event.title:<40} {event.xp_reward:<15} {event.creator_id:<12}")
                if event.description:
                    print(f"      └─ {event.description}")
        
        # Histórico de XP recente
        if xp_count > 0:
            print_section("⭐ Histórico de XP (últimos 10)")
            xp_history = session.exec(
                select(XPHistory).order_by(XPHistory.created_at.desc()).limit(10)
            ).all()
            
            print(f"{'ID':<5} {'User ID':<10} {'Tipo':<15} {'XP':<8} {'Data':<20}")
            print("─" * 80)
            for xp in xp_history:
                date_str = xp.created_at.strftime('%d/%m/%Y %H:%M')
                print(f"{xp.id:<5} {xp.user_id:<10} {xp.type:<15} {xp.xp_amount:<8} {date_str:<20}")
        
        # Rankings
        if user_count > 0:
            print_section("🏆 Top 5 Ranking por Pontos")
            top_users = session.exec(
                select(UserProfile).order_by(UserProfile.pontos.desc()).limit(5)
            ).all()
            
            for idx, user in enumerate(top_users, 1):
                medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "  "
                print(f"{medal} #{idx:<3} {user.username:<20} - {user.pontos} pontos (Nível {user.nivel})")
    
    print_header("✅ Banco de dados funcionando corretamente!")
    print("\n💡 Dica: Use 'python3 verify_database.py' para executar testes automatizados.")
    print()


def main():
    """Função principal"""
    try:
        init_db()
        display_database_info()
    except Exception as e:
        print(f"\n❌ Erro ao acessar banco de dados: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
