import logging
from telegram import Update
from telegram.ext import ContextTypes
from handlers.base import authorized_only
from utils.chat_cleaner import schedule_delete

logger = logging.getLogger(__name__)

@authorized_only
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Master ativo.\nComandos disponíveis: /help")

@authorized_only
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "/status_dexyln – estado do Dexyln\n"
        "/restart_dexyln – reinicia Dexyln\n"
        "/logs_dexyln – logs Dexyln\n"
        "/reboot – reinicia servidor\n"
        "/help – esta ajuda\n\n"
        "Comandos antigos também funcionam."
    )
    await update.message.reply_text(texto)

@authorized_only
async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reboot direto."""
    chat_id = update.effective_chat.id
    msg = await update.message.reply_text("🔄 Reiniciando servidor em 5 segundos...")
    schedule_delete(context, chat_id, msg.message_id, 10)
    context.job_queue.run_once(execute_reboot, 5, context={"chat_id": chat_id})

async def execute_reboot(job):
    chat_id = job.context["chat_id"]
    try:
        import subprocess
        subprocess.run(["sudo", "/usr/sbin/reboot"], check=True, timeout=10)
    except Exception as e:
        logger.error(f"Erro reboot: {e}")