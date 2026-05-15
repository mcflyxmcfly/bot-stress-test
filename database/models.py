"""
Modelos de banco de dados
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class TestRecord(Base):
    """Modelo para registrar testes executados"""
    __tablename__ = 'test_records'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    url = Column(String(500), nullable=False)
    threads = Column(Integer, nullable=False)
    rps = Column(Integer, nullable=False)
    duracao = Column(Integer, nullable=False)
    
    requisicoes_totais = Column(Integer, default=0)
    requisicoes_sucesso = Column(Integer, default=0)
    requisicoes_falha = Column(Integer, default=0)
    tempo_medio_resposta = Column(Float, default=0)
    taxa_erro = Column(Float, default=0)
    
    status_codes = Column(Text, default='{}')  # JSON
    status = Column(String(50), default='pendente')  # pendente, executando, concluído, erro
    mensagem_erro = Column(Text, nullable=True)
    
    data_inicio = Column(DateTime, default=datetime.now)
    data_fim = Column(DateTime, nullable=True)

class BotStatus(Base):
    """Modelo para status do bot"""
    __tablename__ = 'bot_status'
    
    id = Column(Integer, primary_key=True)
    testes_executados = Column(Integer, default=0)
    ativo = Column(Integer, default=1)
    data_inicio = Column(DateTime, default=datetime.now)
    ultima_atualizacao = Column(DateTime, default=datetime.now, onupdate=datetime.now)
