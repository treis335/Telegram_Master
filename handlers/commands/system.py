import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from handlers.base import authorized_only
from utils.shell import run_cmd
from utils.chat_cleaner import schedule_delete

@authorized_only
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    await update.message.reply_text(
        "🤖 Bot Master ativo.\nComandos disponíveis: /help"
    )

@authorized_only
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    texto = (
        "/status_dexyln – estado do bot de arbitragem (Dexyln)\n"
        "/restart_dexyln – reinicia o bot de arbitragem (Dexyln)\n"
        "/logs_dexyln – últimos logs do bot de arbitragem (Dexyln)\n"
        "/reboot – reinicia o servidor\n"
        "/help – mostra esta ajuda\n\n"
        "Os comandos antigos /status_arb, /restart_arb, /logs_arb também funcionam.\n"
        "As mensagens são auto‑apagadas após alguns minutos."
    )
    await update.message.reply_text(texto)

@authorized_only
async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reboot direto."""
    msg = await update.message.reply_text("🔄 Reiniciando servidor em 5 segundos...")
    schedule_delete(context, update.effective_chat.id, msg.message_id, 10)
    context.job_queue.run_once(execute_reboot, 5, context={"chat_id": update.effective_chat.id})

async def execute_reboot(job):
    chat_id = job.context["chat_id"]
    bot = job.context.get("bot")
    try:
        if bot:
            await bot.send_message(chat_id, "💤 A reiniciar agora...")
    except:
        pass
    import os
    os.system("sudo /usr/sbin/reboot")