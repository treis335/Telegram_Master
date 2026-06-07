import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from handlers.commands import system, arbitragem

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
AUTHORIZED_ID = int(os.getenv("AUTHORIZED_USER_ID"))

logging.basicConfig(level=logging.INFO)

def main():
    app = Application.builder().token(TOKEN).build()

    # Sistema
    app.add_handler(CommandHandler("start", system.start))
    app.add_handler(CommandHandler("help", system.help_cmd))
    app.add_handler(CommandHandler("status_arb", arbitragem.status))
    app.add_handler(CommandHandler("restart_arb", arbitragem.restart))
    app.add_handler(CommandHandler("logs_arb", arbitragem.logs))

    # (Aqui adicionas outros handlers futuros)

    logging.info("Bot Master iniciado")
    app.run_polling()

if __name__ == "__main__":
    main()