#!/usr/bin/env python3
"""
Script para verificar se o código atual está funcionando em conjunto com o banco de dados.
Este script testa a conexão com o banco de dados e realiza operações CRUD básicas.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from sqlmodel import Session, select
from app.database import engine, init_db, DATABASE_URL
from app.models import UserProfile, Community, Event, XPHistory, CommunityMembership
from app.auth import hash_password, verify_password


class DatabaseVerifier:
    """Classe para verificar a funcionalidade do banco de dados"""
    
    def __init__(self):
        self.results = []
        self.errors = []
        
    def log_success(self, test_name: str, message: str = ""):
        """Registra um teste bem-sucedido"""
        self.results.append(f"✅ {test_name}: {message if message else 'OK'}")
        print(f"✅ {test_name}: {message if message else 'OK'}")
        
    def log_error(self, test_name: str, error: str):
        """Registra um erro"""
        self.errors.append(f"❌ {test_name}: {error}")
        print(f"❌ {test_name}: {error}")
        
    def test_database_connection(self) -> bool:
        """Testa a conexão com o banco de dados"""
        try:
            with Session(engine) as session:
                # Tenta executar uma query simples
                session.exec(select(UserProfile).limit(1))
            self.log_success("Conexão com banco de dados", f"URL: {DATABASE_URL}")
            return True
        except Exception as e:
            self.log_error("Conexão com banco de dados", str(e))
            return False
            
    def test_table_creation(self) -> bool:
        """Testa a criação de tabelas"""
        try:
            init_db()
            self.log_success("Criação de tabelas", "Todas as tabelas foram criadas/verificadas")
            return True
        except Exception as e:
            self.log_error("Criação de tabelas", str(e))
            return False
            
    def test_user_crud(self) -> bool:
        """Testa operações CRUD para UserProfile"""
        try:
            with Session(engine) as session:
                # CREATE
                test_user = UserProfile(
                    username=f"test_user_{datetime.now().timestamp()}",
                    email=f"test_{datetime.now().timestamp()}@example.com",
                    password_hash=hash_password("test123"),
                    name="Test User",
                    phone="(11) 98765-4321"
                )
                session.add(test_user)
                session.commit()
                session.refresh(test_user)
                user_id = test_user.id
                self.log_success("CREATE User", f"Criado usuário ID: {user_id}")
                
                # READ
                user = session.get(UserProfile, user_id)
                assert user is not None
                assert user.username == test_user.username
                self.log_success("READ User", f"Lido usuário: {user.username}")
                
                # UPDATE
                user.pontos = 100
                user.adicionar_pontos(50)  # Adiciona 50 pontos
                session.add(user)
                session.commit()
                session.refresh(user)
                assert user.pontos == 150
                assert user.nivel == 2  # 150 pontos = nível 2
                self.log_success("UPDATE User", f"Atualizado pontos: {user.pontos}, nível: {user.nivel}")
                
                # DELETE
                session.delete(user)
                session.commit()
                deleted_user = session.get(UserProfile, user_id)
                assert deleted_user is None
                self.log_success("DELETE User", f"Deletado usuário ID: {user_id}")
                
            return True
        except Exception as e:
            self.log_error("CRUD User", str(e))
            return False
            
    def test_community_crud(self) -> bool:
        """Testa operações CRUD para Community"""
        try:
            with Session(engine) as session:
                # CREATE
                test_community = Community(
                    slug=f"test_community_{int(datetime.now().timestamp())}",
                    name="Test Community",
                    description="A test community",
                    visibility="public"
                )
                session.add(test_community)
                session.commit()
                session.refresh(test_community)
                comm_id = test_community.id
                self.log_success("CREATE Community", f"Criada comunidade ID: {comm_id}")
                
                # READ
                community = session.get(Community, comm_id)
                assert community is not None
                assert community.slug == test_community.slug
                self.log_success("READ Community", f"Lida comunidade: {community.name}")
                
                # UPDATE
                community.description = "Updated description"
                session.add(community)
                session.commit()
                session.refresh(community)
                assert community.description == "Updated description"
                self.log_success("UPDATE Community", "Descrição atualizada")
                
                # DELETE
                session.delete(community)
                session.commit()
                deleted_comm = session.get(Community, comm_id)
                assert deleted_comm is None
                self.log_success("DELETE Community", f"Deletada comunidade ID: {comm_id}")
                
            return True
        except Exception as e:
            self.log_error("CRUD Community", str(e))
            return False
            
    def test_event_crud(self) -> bool:
        """Testa operações CRUD para Event"""
        try:
            with Session(engine) as session:
                # Criar um usuário para associar ao evento
                temp_user = UserProfile(
                    username=f"event_creator_{datetime.now().timestamp()}",
                    email=f"creator_{datetime.now().timestamp()}@example.com",
                    password_hash=hash_password("test123"),
                    name="Event Creator"
                )
                session.add(temp_user)
                session.commit()
                session.refresh(temp_user)
                
                # CREATE
                test_event = Event(
                    creator_id=temp_user.id,
                    title="Test Event",
                    description="A test event",
                    xp_reward=50
                )
                session.add(test_event)
                session.commit()
                session.refresh(test_event)
                event_id = test_event.id
                self.log_success("CREATE Event", f"Criado evento ID: {event_id}")
                
                # READ
                event = session.get(Event, event_id)
                assert event is not None
                assert event.title == test_event.title
                self.log_success("READ Event", f"Lido evento: {event.title}")
                
                # UPDATE
                event.xp_reward = 100
                session.add(event)
                session.commit()
                session.refresh(event)
                assert event.xp_reward == 100
                self.log_success("UPDATE Event", f"Recompensa atualizada: {event.xp_reward} XP")
                
                # DELETE
                session.delete(event)
                session.delete(temp_user)
                session.commit()
                self.log_success("DELETE Event", f"Deletado evento ID: {event_id}")
                
            return True
        except Exception as e:
            self.log_error("CRUD Event", str(e))
            return False
            
    def test_xp_history(self) -> bool:
        """Testa o registro de histórico de XP"""
        try:
            with Session(engine) as session:
                # Criar um usuário
                temp_user = UserProfile(
                    username=f"xp_user_{datetime.now().timestamp()}",
                    email=f"xp_{datetime.now().timestamp()}@example.com",
                    password_hash=hash_password("test123"),
                    name="XP User"
                )
                session.add(temp_user)
                session.commit()
                session.refresh(temp_user)
                
                # Criar histórico de XP
                xp_entry = XPHistory(
                    user_id=temp_user.id,
                    type="manual",
                    xp_amount=50,
                    meta='{"reason": "test"}'
                )
                session.add(xp_entry)
                session.commit()
                session.refresh(xp_entry)
                self.log_success("CREATE XP History", f"Criado registro XP ID: {xp_entry.id}")
                
                # Ler histórico
                history = session.exec(
                    select(XPHistory).where(XPHistory.user_id == temp_user.id)
                ).all()
                assert len(history) > 0
                self.log_success("READ XP History", f"Encontrados {len(history)} registros")
                
                # Limpar (deletar XP history antes do usuário por causa da foreign key)
                session.delete(xp_entry)
                session.commit()
                session.delete(temp_user)
                session.commit()
                
            return True
        except Exception as e:
            self.log_error("XP History", str(e))
            return False
            
    def test_community_membership(self) -> bool:
        """Testa o relacionamento de membros em comunidades"""
        try:
            with Session(engine) as session:
                # Criar usuário e comunidade
                temp_user = UserProfile(
                    username=f"member_{datetime.now().timestamp()}",
                    email=f"member_{datetime.now().timestamp()}@example.com",
                    password_hash=hash_password("test123"),
                    name="Member User"
                )
                temp_community = Community(
                    slug=f"member_comm_{int(datetime.now().timestamp())}",
                    name="Member Community",
                    description="Test community for membership"
                )
                session.add_all([temp_user, temp_community])
                session.commit()
                session.refresh(temp_user)
                session.refresh(temp_community)
                
                # Criar membership
                membership = CommunityMembership(
                    community_id=temp_community.id,
                    user_id=temp_user.id,
                    role="member"
                )
                session.add(membership)
                session.commit()
                session.refresh(membership)
                self.log_success("CREATE Membership", f"Criada associação ID: {membership.id}")
                
                # Verificar membership
                memberships = session.exec(
                    select(CommunityMembership).where(
                        CommunityMembership.user_id == temp_user.id
                    )
                ).all()
                assert len(memberships) > 0
                self.log_success("READ Membership", f"Usuário é membro de {len(memberships)} comunidade(s)")
                
                # Limpar (deletar membership antes da comunidade e usuário por causa da foreign key)
                session.delete(membership)
                session.commit()
                session.delete(temp_community)
                session.delete(temp_user)
                session.commit()
                
            return True
        except Exception as e:
            self.log_error("Community Membership", str(e))
            return False
            
    def test_password_hashing(self) -> bool:
        """Testa hash e verificação de senha"""
        try:
            password = "test_password_123"
            hashed = hash_password(password)
            
            # Verificar que a senha hasheada é diferente da original
            assert hashed != password
            self.log_success("Password Hash", "Senha hasheada corretamente")
            
            # Verificar que a senha correta é validada
            assert verify_password(password, hashed)
            self.log_success("Password Verify", "Senha verificada corretamente")
            
            # Verificar que senha incorreta não é validada
            assert not verify_password("wrong_password", hashed)
            self.log_success("Password Rejection", "Senha incorreta rejeitada corretamente")
            
            return True
        except Exception as e:
            self.log_error("Password Hashing", str(e))
            return False
            
    def test_user_level_calculation(self) -> bool:
        """Testa o cálculo automático de nível baseado em pontos"""
        try:
            with Session(engine) as session:
                # Criar usuário
                test_user = UserProfile(
                    username=f"level_user_{datetime.now().timestamp()}",
                    email=f"level_{datetime.now().timestamp()}@example.com",
                    password_hash=hash_password("test123"),
                    name="Level User",
                    pontos=0,
                    nivel=1
                )
                session.add(test_user)
                session.commit()
                session.refresh(test_user)
                
                # Verificar nível inicial
                assert test_user.nivel == 1
                self.log_success("Level Calculation", "Nível inicial: 1")
                
                # Adicionar 150 pontos (deve ser nível 2)
                test_user.adicionar_pontos(150)
                session.add(test_user)
                session.commit()
                session.refresh(test_user)
                assert test_user.pontos == 150
                assert test_user.nivel == 2
                self.log_success("Level Calculation", "150 pontos = Nível 2")
                
                # Adicionar mais 250 pontos (total 400 = nível 5)
                test_user.adicionar_pontos(250)
                session.add(test_user)
                session.commit()
                session.refresh(test_user)
                assert test_user.pontos == 400
                assert test_user.nivel == 5
                self.log_success("Level Calculation", "400 pontos = Nível 5")
                
                # Limpar
                session.delete(test_user)
                session.commit()
                
            return True
        except Exception as e:
            self.log_error("Level Calculation", str(e))
            return False
            
    def run_all_tests(self):
        """Executa todos os testes"""
        print("\n" + "="*70)
        print("🔍 VERIFICAÇÃO DE BANCO DE DADOS - PenseOffline")
        print("="*70 + "\n")
        
        print(f"📊 Banco de dados: {DATABASE_URL}\n")
        
        tests = [
            ("Criação de Tabelas", self.test_table_creation),
            ("Conexão", self.test_database_connection),
            ("CRUD de Usuários", self.test_user_crud),
            ("CRUD de Comunidades", self.test_community_crud),
            ("CRUD de Eventos", self.test_event_crud),
            ("Histórico de XP", self.test_xp_history),
            ("Membros de Comunidade", self.test_community_membership),
            ("Hash de Senha", self.test_password_hashing),
            ("Cálculo de Nível", self.test_user_level_calculation),
        ]
        
        print("🧪 Executando testes...\n")
        
        for test_name, test_func in tests:
            print(f"\n--- Testando: {test_name} ---")
            test_func()
            
        print("\n" + "="*70)
        print("📈 RESUMO DOS TESTES")
        print("="*70 + "\n")
        
        total_tests = len(tests)
        successful_tests = len([r for r in self.results if r.startswith("✅")])
        failed_tests = len(self.errors)
        
        print(f"Total de testes: {total_tests}")
        print(f"✅ Testes bem-sucedidos: {successful_tests}")
        print(f"❌ Testes com falha: {failed_tests}")
        
        if self.errors:
            print("\n⚠️  ERROS ENCONTRADOS:")
            for error in self.errors:
                print(f"  {error}")
        
        print("\n" + "="*70)
        
        if failed_tests == 0:
            print("✨ TODOS OS TESTES PASSARAM! O banco de dados está funcionando corretamente.")
            print("="*70 + "\n")
            return 0
        else:
            print("⚠️  ALGUNS TESTES FALHARAM. Verifique os erros acima.")
            print("="*70 + "\n")
            return 1


def main():
    """Função principal"""
    verifier = DatabaseVerifier()
    exit_code = verifier.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
