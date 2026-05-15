"""
Gerenciamento do banco de dados
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database.models import Base
from utils.config import DATABASE_URL
from utils.logger import logger

# Criar engine
engine = create_engine(DATABASE_URL, echo=False)

# Criar session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Inicializar banco de dados"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")

def get_db() -> Session:
    """Obter nova sessão do banco de dados"""
    return SessionLocal()
