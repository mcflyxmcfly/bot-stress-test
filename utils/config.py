"""
Configurações do bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Token do Telegram Bot
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN não configurado no .env")

# ID do admin
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))

# Limites de teste
MAX_THREADS = 100
MAX_RPS = 10000
MIN_DURACAO = 10
MAX_DURACAO = 3600

# Banco de dados
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_stress_test.db')

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
