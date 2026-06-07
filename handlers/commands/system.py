from telegram import Update
from telegram.ext import ContextTypes
from handlers.base import authorized_only
from utils.shell import run_cmd

@authorized_only
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot Master ativo.\nComandos disponíveis: /help"
    )

@authorized_only
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "/status_arb – estado do bot de arbitragem\n"
        "/restart_arb – reinicia o bot de arbitragem\n"
        "/logs_arb – últimos 30 logs do bot de arbitragem\n"
        "(em breve: comandos para outros bots)"
    )
    await update.message.reply_text(texto)