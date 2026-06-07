import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from handlers.commands import system, dexyln
from handlers.commands.system import reboot, reboot_confirm, cancel, WAITING_CONFIRMATION

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

    # Comandos base (sem conversação)
    app.add_handler(CommandHandler("start", system.start))
    app.add_handler(CommandHandler("help", system.help_cmd))

    # ConversationHandler para reboot
    reboot_handler = ConversationHandler(
        entry_points=[CommandHandler("reboot", reboot)],
        states={
            WAITING_CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, reboot_confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(reboot_handler)

    # Comandos do bot Dexyln (novos nomes)
    app.add_handler(CommandHandler("status_dexyln", dexyln.status))
    app.add_handler(CommandHandler("restart_dexyln", dexyln.restart))
    app.add_handler(CommandHandler("logs_dexyln", dexyln.logs))

    # Compatibilidade com nomes antigos
    app.add_handler(CommandHandler("status_arb", dexyln.status))
    app.add_handler(CommandHandler("restart_arb", dexyln.restart))
    app.add_handler(CommandHandler("logs_arb", dexyln.logs))

    logging.info("Bot Master iniciado")
    app.run_polling()

if __name__ == "__main__":
    main()