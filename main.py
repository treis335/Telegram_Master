import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

# Carrega variáveis do ficheiro .env
load_dotenv()

# Lê as variáveis de ambiente
TOKEN = os.getenv("TELEGRAM_TOKEN")
AUTHORIZED_ID = os.getenv("AUTHORIZED_USER_ID")

# Validação
if not TOKEN:
    raise ValueError("ERRO: Variável TELEGRAM_TOKEN não definida no ficheiro .env")
if not AUTHORIZED_ID:
    raise ValueError("ERRO: Variável AUTHORIZED_USER_ID não definida no ficheiro .env")

AUTHORIZED_ID = int(AUTHORIZED_ID)

# Configura logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Import handlers (depois de validar as variáveis, pois eles também as usam)
from handlers.commands import system, arbitragem

def main():
    app = Application.builder().token(TOKEN).build()

    # Comandos do sistema
    app.add_handler(CommandHandler("start", system.start))
    app.add_handler(CommandHandler("help", system.help_cmd))

    # Comandos do bot de arbitragem
    app.add_handler(CommandHandler("status_arb", arbitragem.status))
    app.add_handler(CommandHandler("restart_arb", arbitragem.restart))
    app.add_handler(CommandHandler("logs_arb", arbitragem.logs))

    logging.info("Bot Master iniciado")
    app.run_polling()

if __name__ == "__main__":
    main()