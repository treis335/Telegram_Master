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
        "/status_dexyln – estado do bot de arbitragem (Dexyln)\n"
        "/restart_dexyln – reinicia o bot de arbitragem (Dexyln)\n"
        "/logs_dexyln – últimos logs do bot de arbitragem (Dexyln)\n"
        "/reboot – reinicia o servidor completo\n"
        "/help – mostra esta ajuda\n\n"
        "Os comandos antigos /status_arb, /restart_arb, /logs_arb também funcionam."
    )
    await update.message.reply_text(texto)

@authorized_only
async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ O servidor vai reiniciar em 5 segundos. A ligação SSH será perdida.")
    import asyncio
    await asyncio.sleep(5)
    await update.message.reply_text("🔄 A reiniciar...")
    run_cmd("sudo reboot")