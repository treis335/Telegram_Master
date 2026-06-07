import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from handlers.commands import system, dexyln
from handlers.commands.system import reboot

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
AUTHORIZED_ID = os.getenv("AUTHORIZED_USER_ID")

if not TOKEN:
    raise ValueError("ERRO: TELEGRAM_TOKEN não definido no .env")
if not AUTHORIZED_ID:
    raise ValueError("ERRO: AUTHORIZED_USER_ID não definido no .env")

AUTHORIZED_ID = int(AUTHORIZED_ID)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    app = Application.builder().token(TOKEN).build()

    # Comandos base
    app.add_handler(CommandHandler("start", system.start))
    app.add_handler(CommandHandler("help", system.help_cmd))
    app.add_handler(CommandHandler("reboot", reboot))

    # Comandos Dexyln
    app.add_handler(CommandHandler("status_dexyln", dexyln.status))
    app.add_handler(CommandHandler("restart_dexyln", dexyln.restart))
    app.add_handler(CommandHandler("logs_dexyln", dexyln.logs))

    # Compatibilidade antiga
    app.add_handler(CommandHandler("status_arb", dexyln.status))
    app.add_handler(CommandHandler("restart_arb", dexyln.restart))
    app.add_handler(CommandHandler("logs_arb", dexyln.logs))

    logging.info("Bot Master iniciado")
    app.run_polling()

if __name__ == "__main__":
    main()