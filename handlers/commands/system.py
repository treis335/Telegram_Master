import logging
from telegram import Update
from telegram.ext import ContextTypes
from handlers.base import authorized_only
from utils.chat_cleaner import schedule_delete

logger = logging.getLogger(__name__)

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
        "As mensagens são auto-apagadas após alguns minutos."
    )
    await update.message.reply_text(texto)

@authorized_only
async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reboot direto sem confirmação."""
    chat_id = update.effective_chat.id
    msg = await update.message.reply_text("🔄 Reiniciando servidor em 5 segundos...")
    schedule_delete(context, chat_id, msg.message_id, 10)

    # Agenda o reboot
    context.job_queue.run_once(execute_reboot, 5, context={"chat_id": chat_id})

async def execute_reboot(job):
    """Executa o reboot do sistema."""
    chat_id = job.context["chat_id"]
    bot = job.context.get("bot") or job.get_bot()

    try:
        if bot:
            await bot.send_message(chat_id, "💤 A reiniciar agora...")
    except:
        pass

    try:
        import subprocess
        subprocess.run(["sudo", "/usr/sbin/reboot"], check=True, timeout=10)
    except Exception as e:
        logger.error(f"Erro ao executar reboot: {e}")
        try:
            if bot:
                await bot.send_message(chat_id, f"❌ Erro no reboot: {e}")
        except:
            pass