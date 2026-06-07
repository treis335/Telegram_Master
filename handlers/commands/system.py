import asyncio
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from handlers.base import authorized_only
from utils.shell import run_cmd
from utils.chat_cleaner import schedule_delete

WAITING_CONFIRMATION = 1

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
        "/reboot – reinicia o servidor (com confirmação)\n"
        "/help – mostra esta ajuda\n\n"
        "Os comandos antigos /status_arb, /restart_arb, /logs_arb também funcionam.\n"
        "As mensagens são auto‑apagadas após alguns minutos."
    )
    await update.message.reply_text(texto)

@authorized_only
async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia o pedido de confirmação."""
    msg = await update.message.reply_text(
        "⚠️ Atenção: o servidor vai reiniciar. Tem a certeza?\n"
        "Responda com *sim* ou *não* (ou /cancel para cancelar).",
        parse_mode="Markdown"
    )
    schedule_delete(context, update.effective_chat.id, msg.message_id, 60)
    return WAITING_CONFIRMATION

@authorized_only
async def reboot_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa a resposta e agenda o reboot se for sim."""
    answer = update.message.text.strip().lower()
    chat_id = update.effective_chat.id
    user_msg_id = update.message.message_id

    schedule_delete(context, chat_id, user_msg_id, 5)

    if answer in ["sim", "s", "yes", "y"]:
        confirm_msg = await update.message.reply_text("🔄 O servidor vai reiniciar em 5 segundos...")
        schedule_delete(context, chat_id, confirm_msg.message_id, 10)
        # Agenda o reboot usando JobQueue
        context.job_queue.run_once(execute_reboot, 5, context={"chat_id": chat_id, "bot": context.bot})
    else:
        cancel_msg = await update.message.reply_text("✅ Reboot cancelado.")
        schedule_delete(context, chat_id, cancel_msg.message_id, 10)

    return ConversationHandler.END

async def execute_reboot(job):
    chat_id = job.context["chat_id"]
    bot = job.context.get("bot")
    try:
        if bot:
            await bot.send_message(chat_id, "💤 A reiniciar agora...")
    except:
        pass
    import os
    os.system("sudo /usr/sbin/reboot")  # mais direto que subprocess

@authorized_only
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operação cancelada.")
    return ConversationHandler.END