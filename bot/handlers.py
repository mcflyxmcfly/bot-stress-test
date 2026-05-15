"""
Handlers dos comandos do Telegram
"""
import asyncio
import json
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.stress_tester import StressTester
from bot.reports import RelatorioGenerator
from database.models import TestRecord, BotStatus
from database.db import SessionLocal, get_db
from utils.logger import logger
from utils.config import MAX_THREADS, MAX_RPS, MIN_DURACAO, MAX_DURACAO

# Armazenar contexto do teste por usuário
testes_em_progresso = {}
tempo_inicio_bot = datetime.now()

# Mensagem de boas-vindas com aviso ético
MENSAGEM_BOAS_VINDAS = """
🚨 ⚠️ AVISO ÉTICO IMPORTANTE ⚠️ 🚨

Bem-vindo ao Bot de Teste de Stress/Penetração!

Este bot é uma ferramenta legítima de teste de carga. VOCÊ DEVE TER AUTORIZAÇÃO EXPLÍCITA do proprietário do servidor ANTES de realizar qualquer teste.

✅ USE APENAS EM:
   • Seus próprios servidores
   • Ambientes de desenvolvimento/teste
   • Servidores com autorização expressa

❌ NÃO USE EM:
   • Servidores de terceiros sem autorização
   • Ambientes de produção não autorizados
   • Qualquer sistema que você não tem direito de testar

⚖️ Uso não autorizado é ILEGAL e sujeito a penalidades.

═══════════════════════════════════════════════════════════════

Clique em um botão abaixo para continuar:
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start - Mostrar menu principal"""
    
    user_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton("🚀 Iniciar Teste", callback_data='iniciar_teste')],
        [InlineKeyboardButton("📊 Histórico", callback_data='historico'), 
         InlineKeyboardButton("📈 Uptime", callback_data='uptime')],
        [InlineKeyboardButton("❓ Ajuda", callback_data='ajuda'),
         InlineKeyboardButton("📋 Comandos", callback_data='comandos')],
        [InlineKeyboardButton("ℹ️ Sobre", callback_data='sobre')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        MENSAGEM_BOAS_VINDAS,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    
    logger.info(f"Usuário {user_id} iniciou o bot")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para botões inline"""
    
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == 'iniciar_teste':
        await iniciar_teste_handler(query, context)
    elif query.data == 'historico':
        await historico_handler(query, context)
    elif query.data == 'uptime':
        await uptime_handler(query, context)
    elif query.data == 'ajuda':
        await ajuda_handler(query, context)
    elif query.data == 'comandos':
        await comandos_handler(query, context)
    elif query.data == 'sobre':
        await sobre_handler(query, context)

async def iniciar_teste_handler(query, context):
    """Iniciar novo teste"""
    
    user_id = query.from_user.id
    
    keyboard = [
        [InlineKeyboardButton("❌ Cancelar", callback_data='menu_principal')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    mensagem = """
🔗 Digite a URL que deseja testar:

Exemplo: https://exemplo.com
"""
    
    await query.edit_message_text(text=mensagem, reply_markup=reply_markup)
    
    # Armazenar estado para próxima mensagem
    context.user_data['etapa_teste'] = 'url'
    logger.info(f"Usuário {user_id} iniciando novo teste")

async def historico_handler(query, context):
    """Mostrar histórico de testes"""
    
    user_id = query.from_user.id
    db = get_db()
    
    try:
        testes = db.query(TestRecord).filter(TestRecord.user_id == user_id).order_by(TestRecord.data_inicio.desc()).limit(5).all()
        
        if not testes:
            mensagem = "❌ Você ainda não realizou nenhum teste."
        else:
            mensagem = "📊 Últimos 5 testes:\n\n"
            for teste in testes:
                mensagem += f"ID: {teste.id}\n"
                mensagem += f"URL: {teste.url}\n"
                mensagem += f"Data: {teste.data_inicio.strftime('%d/%m/%Y %H:%M')}\n"
                mensagem += f"Status: {teste.status}\n"
                mensagem += f"Requisições: {teste.requisicoes_totais}\n"
                mensagem += "─" * 40 + "\n"
        
        keyboard = [
            [InlineKeyboardButton("🔙 Menu Principal", callback_data='menu_principal')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text=mensagem, reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Erro ao buscar histórico: {e}")
        await query.edit_message_text(f"❌ Erro ao buscar histórico: {e}")
    finally:
        db.close()

async def uptime_handler(query, context):
    """Mostrar uptime do bot"""
    
    db = get_db()
    try:
        status = db.query(BotStatus).first()
        
        if status:
            uptime = datetime.now() - status.data_inicio
            horas = uptime.total_seconds() // 3600
            minutos = (uptime.total_seconds() % 3600) // 60
        else:
            horas = minutos = 0
            status = BotStatus()
            db.add(status)
            db.commit()
        
        mensagem = f"""
⏱️ STATUS DO BOT

Uptime: {int(horas)}h {int(minutos)}m
Testes Executados: {status.testes_executados}
Status: {'🟢 Online' if status.ativo else '🔴 Offline'}
Última Atualização: {status.ultima_atualizacao.strftime('%d/%m/%Y %H:%M:%S')}
"""
        
        keyboard = [
            [InlineKeyboardButton("🔙 Menu Principal", callback_data='menu_principal')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text=mensagem, reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Erro ao buscar uptime: {e}")
        await query.edit_message_text(f"❌ Erro: {e}")
    finally:
        db.close()

async def ajuda_handler(query, context):
    """Mostrar ajuda"""
    
    mensagem = """
❓ AJUDA

Como usar o bot:

1️⃣ Clique em "🚀 Iniciar Teste"
2️⃣ Digite a URL (ex: https://exemplo.com)
3️⃣ Digite o número de threads (1-100)
4️⃣ Digite o RPS (Requisições/Segundo)
5️⃣ Digite a duração (10-3600 segundos)
6️⃣ O bot executará o teste e enviará um relatório

Cada teste será salvo no histórico.
"""
    
    keyboard = [
        [InlineKeyboardButton("🔙 Menu Principal", callback_data='menu_principal')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=mensagem, reply_markup=reply_markup)

async def comandos_handler(query, context):
    """Mostrar comandos disponíveis"""
    
    mensagem = """
📋 COMANDOS DISPONÍVEIS

/start - Mostrar menu principal
/teste - Atalho para iniciar novo teste
/historico - Ver histórico de testes
/uptime - Status do bot
/ajuda - Mostrar esta ajuda
/relatorio [id] - Ver relatório detalhado
"""
    
    keyboard = [
        [InlineKeyboardButton("🔙 Menu Principal", callback_data='menu_principal')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=mensagem, reply_markup=reply_markup)

async def sobre_handler(query, context):
    """Mostrar informações sobre o bot"""
    
    mensagem = """
ℹ️ SOBRE

Bot Stress Test v1.0

Ferramenta ética de teste de carga/penetração integrada com Telegram.

📌 RECURSOS:
   • Testes de stress configuráveis
   • Relatórios detalhados
   • Histórico de testes
   • Monitoramento de uptime
   • Interface intuitiva

⚖️ AVISO:
   Use apenas em sistemas autorizados!
   Proibido uso não autorizado.

Desenvolvido com Python + Telegram Bot API
"""
    
    keyboard = [
        [InlineKeyboardButton("🔙 Menu Principal", callback_data='menu_principal')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=mensagem, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para mensagens de texto"""
    
    user_id = update.effective_user.id
    mensagem = update.message.text.strip()
    
    etapa = context.user_data.get('etapa_teste')
    
    if etapa == 'url':
        # Validar URL
        if not mensagem.startswith(('http://', 'https://')):
            await update.message.reply_text("❌ URL inválida. Deve começar com http:// ou https://")
            return
        
        context.user_data['url'] = mensagem
        context.user_data['etapa_teste'] = 'threads'
        
        await update.message.reply_text(f"""
✅ URL: {mensagem}

⚙️ Agora digite o número de THREADS (1-{MAX_THREADS}):
""")
    
    elif etapa == 'threads':
        try:
            threads = int(mensagem)
            if not (1 <= threads <= MAX_THREADS):
                raise ValueError()
            
            context.user_data['threads'] = threads
            context.user_data['etapa_teste'] = 'rps'
            
            await update.message.reply_text(f"""
✅ Threads: {threads}

📊 Agora digite o RPS - Requisições por Segundo (1-{MAX_RPS}):
""")
        except:
            await update.message.reply_text(f"❌ Inválido. Digite um número entre 1 e {MAX_THREADS}")
    
    elif etapa == 'rps':
        try:
            rps = int(mensagem)
            if not (1 <= rps <= MAX_RPS):
                raise ValueError()
            
            context.user_data['rps'] = rps
            context.user_data['etapa_teste'] = 'duracao'
            
            await update.message.reply_text(f"""
✅ RPS: {rps}

⏱️ Agora digite a DURAÇÃO em segundos ({MIN_DURACAO}-{MAX_DURACAO}):
""")
        except:
            await update.message.reply_text(f"❌ Inválido. Digite um número entre 1 e {MAX_RPS}")
    
    elif etapa == 'duracao':
        try:
            duracao = int(mensagem)
            if not (MIN_DURACAO <= duracao <= MAX_DURACAO):
                raise ValueError()
            
            context.user_data['duracao'] = duracao
            
            # Confirmar e executar teste
            await executar_teste(update, context)
            
        except:
            await update.message.reply_text(f"❌ Inválido. Digite um número entre {MIN_DURACAO} e {MAX_DURACAO}")

async def executar_teste(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Executar o teste de stress"""
    
    user_id = update.effective_user.id
    
    url = context.user_data.get('url')
    threads = context.user_data.get('threads')
    rps = context.user_data.get('rps')
    duracao = context.user_data.get('duracao')
    
    if not all([url, threads, rps, duracao]):
        await update.message.reply_text("❌ Dados incompletos. Tente novamente com /teste")
        return
    
    # Criar registro no BD
    db = get_db()
    try:
        teste_record = TestRecord(
            user_id=user_id,
            url=url,
            threads=threads,
            rps=rps,
            duracao=duracao,
            status='executando'
        )
        db.add(teste_record)
        db.commit()
        db.refresh(teste_record)
        
        teste_id = teste_record.id
        
        # Enviar mensagem de inicio
        await update.message.reply_text(f"""
🚀 INICIANDO TESTE #{teste_id}

URL: {url}
Threads: {threads}
RPS: {rps}
Duração: {duracao}s

Aguarde... ⏳
""")
        
        logger.info(f"Iniciando teste #{teste_id} para usuário {user_id}")
        
        # Executar teste em background
        tester = StressTester(url, threads, rps, duracao)
        valida, msg = tester.validar_url()
        
        if not valida:
            teste_record.status = 'erro'
            teste_record.mensagem_erro = msg
            db.commit()
            
            await update.message.reply_text(f"❌ Erro: {msg}")
            logger.error(f"URL inválida: {msg}")
            return
        
        # Executar teste assincronamente
        sucesso, msg = await tester.executar_teste()
        
        # Atualizar registro
        relatorio = tester.obter_relatorio()
        
        teste_record.requisicoes_totais = relatorio['requisicoes_totais']
        teste_record.requisicoes_sucesso = relatorio['requisicoes_sucesso']
        teste_record.requisicoes_falha = relatorio['requisicoes_falha']
        teste_record.tempo_medio_resposta = relatorio['tempo_medio_ms']
        teste_record.taxa_erro = relatorio['taxa_erro_percentual']
        teste_record.status_codes = json.dumps(relatorio['status_codes'])
        teste_record.data_fim = datetime.now()
        teste_record.status = 'concluído' if sucesso else 'erro'
        teste_record.mensagem_erro = msg if not sucesso else None
        
        db.commit()
        
        # Gerar e enviar relatório
        relatorio_texto = RelatorioGenerator.gerar_relatorio_texto(teste_record)
        
        await update.message.reply_text(relatorio_texto)
        
        logger.info(f"Teste #{teste_id} concluído para usuário {user_id}")
        
        # Atualizar bot status
        status = db.query(BotStatus).first()
        if status:
            status.testes_executados += 1
            status.ultima_atualizacao = datetime.now()
            db.commit()
        
        # Limpar contexto
        context.user_data.pop('etapa_teste', None)
        context.user_data.pop('url', None)
        context.user_data.pop('threads', None)
        context.user_data.pop('rps', None)
        context.user_data.pop('duracao', None)
        
    except Exception as e:
        logger.error(f"Erro ao executar teste: {e}")
        await update.message.reply_text(f"❌ Erro ao executar teste: {e}")
        
    finally:
        db.close()

async def comando_teste(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /teste - Atalho para iniciar teste"""
    user_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton("❌ Cancelar", callback_data='menu_principal')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔗 Digite a URL que deseja testar:\n\nExemplo: https://exemplo.com",
        reply_markup=reply_markup
    )
    
    context.user_data['etapa_teste'] = 'url'

async def menu_principal(query, context):
    """Voltar ao menu principal"""
    keyboard = [
        [InlineKeyboardButton("🚀 Iniciar Teste", callback_data='iniciar_teste')],
        [InlineKeyboardButton("📊 Histórico", callback_data='historico'), 
         InlineKeyboardButton("📈 Uptime", callback_data='uptime')],
        [InlineKeyboardButton("❓ Ajuda", callback_data='ajuda'),
         InlineKeyboardButton("📋 Comandos", callback_data='comandos')],
        [InlineKeyboardButton("ℹ️ Sobre", callback_data='sobre')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=MENSAGEM_BOAS_VINDAS, reply_markup=reply_markup)
