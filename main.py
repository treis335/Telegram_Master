import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

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

# Import handlers
from handlers.commands import system, dexyln

def main():
    app = Application.builder().token(TOKEN).build()

    # ConversationHandler para o comando /reboot
    reboot_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("reboot", system.reboot)],
        states={
            system.WAITING_CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, system.reboot_confirm)],
        },
        fallbacks=[CommandHandler("cancel", system.cancel)],
    )
    app.add_handler(reboot_conv_handler)

    # Comandos base (sem confirmação)
    app.add_handler(CommandHandler("start", system.start))
    app.add_handler(CommandHandler("help", system.help_cmd))

    # Comandos para o bot Dexyln (novos nomes)
    app.add_handler(CommandHandler("status_dexyln", dexyln.status))
    app.add_handler(CommandHandler("restart_dexyln", dexyln.restart))
    app.add_handler(CommandHandler("logs_dexyln", dexyln.logs))

    # Compatibilidade com nomes antigos (status_arb, restart_arb, logs_arb)
    app.add_handler(CommandHandler("status_arb", dexyln.status))
    app.add_handler(CommandHandler("restart_arb", dexyln.restart))
    app.add_handler(CommandHandler("logs_arb", dexyln.logs))

    logging.info("Bot Master iniciado com chat cleaner e confirmação para reboot")
    app.run_polling()

if __name__ == "__main__":
    main()