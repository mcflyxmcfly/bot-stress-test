
md
# Bot Stress Test 🚀

Bot de teste de carga/penetração integrado com Telegram. Uma ferramenta **ética** para testar a resistência de seus servidores.

## ⚠️ Aviso Ético Importante

Este bot é uma ferramenta legítima de teste de carga. **Você DEVE ter autorização explícita** do proprietário do servidor ANTES de realizar qualquer teste.

### ✅ USE APENAS EM:
- Seus próprios servidores
- Ambientes de desenvolvimento/teste
- Servidores com autorização expressa

### ❌ NÃO USE EM:
- Servidores de terceiros sem autorização
- Ambientes de produção não autorizados
- Qualquer sistema que você não tem direito de testar

⚖️ **Uso não autorizado é ILEGAL e sujeito a penalidades.**

---

## 🎯 Funcionalidades

- 🚀 **Testes de Stress Configuráveis** - Controle threads, RPS e duração
- 📊 **Relatórios Detalhados** - Requisições aceitas/recusadas, códigos HTTP, tempos de resposta
- 📈 **Histórico de Testes** - Salva e recupera últimos 5 testes
- ⏱️ **Uptime do Bot** - Monitoramento em tempo real
- 🧬 **Motor Assíncrono** - Máxima performance com aiohttp
- 💾 **Banco de Dados** - SQLite automático (sem config necessária)
- 🔒 **Sistema de Logs** - Rastreia todas as ações

---

## 📦 Instalação

### 1. Clone o repositório:
```bash
git clone https://github.com/mcflyxmcfly/bot-stress-test.git
cd bot-stress-test
2. Crie um ambiente virtual:
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
3. Instale as dependências:
bash
pip install -r requirements.txt
4. Configure o .env:
bash
cp .env.example .env
nano .env
Adicione:

Code
TELEGRAM_TOKEN=seu_token_do_bot_aqui
ADMIN_ID=seu_id_telegram_aqui
5. Execute:
bash
python main.py
📱 Como Usar
Procure seu bot no Telegram
Envie /start para ver o menu
Clique em "🚀 Iniciar Teste"
Siga as etapas:
Digite a URL: https://seu-site.com
Digite threads: 10 (1-100)
Digite RPS: 100 (1-10.000 requisições/segundo)
Digite duração: 60 segundos (10-3600)
Receba o relatório completo!
🎮 Comandos
Comando	Descrição
/start	Menu principal
/teste	Atalho rápido para iniciar teste
/historico	Ver últimos 5 testes
/uptime	Status do bot
/ajuda	Instruções de uso
/comandos	Lista de comandos
📊 Relatório de Teste
Exemplo de relatório recebido:

Code
✅ TESTE CONCLUÍDO

📋 INFORMAÇÕES DO TESTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 URL: https://exemplo.com
📅 Data: 15/05/2026 14:30:45
⚙️ Threads: 10
⚡ RPS Configurado: 100
⏳ Duração: 60s

📊 RESULTADOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Requisições Aceitas: 5,850
❌ Requisições Recusadas: 150
📈 Total: 6,000

📉 TAXA DE SUCESSO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Sucesso: 97.50%
❌ Falha: 2.50%

⏱️ TEMPOS DE RESPOSTA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔹 Média: 0.245ms
🔸 Mínimo: 0.052ms
🔴 Máximo: 1.234ms

📊 CÓDIGOS HTTP RETORNADOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
200: 5,850 (97.5%)
503: 100 (1.67%)
TIMEOUT: 50 (0.83%)

🔔 ID do Teste: #1
🛠️ Tecnologias
Python 3.8+
Telegram Bot API (python-telegram-bot)
aiohttp (requisições HTTP assincronamente)
SQLAlchemy (ORM para banco de dados)
SQLite (banco de dados leve)
📁 Estrutura do Projeto
Code
bot-stress-test/
├── main.py                    # Entrada principal
├── bot/
│   ├── handlers.py           # Comandos Telegram
│   ├── stress_tester.py      # Motor de testes
│   └── reports.py            # Gerador de relatórios
├── database/
│   ├── models.py             # Modelos SQLAlchemy
│   └── db.py                 # Gerenciamento BD
├── utils/
│   ├── config.py             # Configurações
│   └── logger.py             # Sistema de logs
├── requirements.txt          # Dependências
└── .env.example              # Template de config
⚙️ Configurações
Edite o arquivo .env para customizar:

env
TELEGRAM_TOKEN=seu_token
ADMIN_ID=seu_id
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///bot_stress_test.db
🚀 Deployment
Codespace:
Clone o repositório
Siga os passos de instalação acima
Execute python main.py
Replit:
Fork este repositório
Configure as variáveis de ambiente (Secrets)
Execute python main.py
VPS/Servidor:
Clone o repositório
Configure um supervisor/systemd para manter rodando
Execute em background
📝 Licença
MIT

👤 Autor
mcflyxmcfly - GitHub

⚠️ Disclaimer
Este software é fornecido "como está", sem garantias de qualquer tipo. O autor não é responsável por:

Uso não autorizado em servidores terceirizados
Danos causados pelo uso inadequado
Violação de leis aplicáveis
Use com responsabilidade e ética.
