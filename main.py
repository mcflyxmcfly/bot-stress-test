"""
Aplicação principal - Bot de Teste de Stress
"""
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from bot.handlers import (
    start, button_callback, handle_message, comando_teste, menu_principal
)
from database.db import init_db
from utils.config import TELEGRAM_TOKEN
from utils.logger import logger

def main():
    """Função principal"""
    
    # Inicializar banco de dados
    logger.info("Inicializando banco de dados...")
    init_db()
    
    # Criar aplicação
    logger.info("Iniciando bot...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Adicionar handlers de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("teste", comando_teste))
    
    # Handlers de callbacks (botões)
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(CallbackQueryHandler(menu_principal, pattern='^menu_principal$'))
    
    # Handler de mensagens de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Iniciar bot
    logger.info(f"Bot iniciado com sucesso! Escutando por mensagens...")
    
    try:
        app.run_polling()
    except KeyboardInterrupt:
        logger.info("Bot parado pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")

if __name__ == '__main__':
    main()
