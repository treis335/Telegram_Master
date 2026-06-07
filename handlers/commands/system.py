import subprocess
import logging
from telegram import Update
from telegram.ext import ContextTypes
from handlers.base import authorized_only
from utils.chat_cleaner import schedule_delete

logger = logging.getLogger(__name__)

@authorized_only
async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reboot direto."""
    chat_id = update.effective_chat.id
    msg = await update.message.reply_text("🔄 Reiniciando servidor em 5 segundos...")
    schedule_delete(context, chat_id, msg.message_id, 10)
    context.job_queue.run_once(execute_reboot, 5, context={"chat_id": chat_id})

async def execute_reboot(job):
    """Função chamada após 5 segundos para executar o reboot."""
    chat_id = job.context["chat_id"]
    try:
        logger.info(f"Tentando reiniciar o servidor após comando do chat {chat_id}")
        # Usa shell=True para simular um terminal e /usr/bin/sudo para garantir o PATH correto
        subprocess.run("/usr/bin/sudo /usr/sbin/reboot", shell=True, check=True, timeout=10)
        logger.info("Comando reboot executado com sucesso.")
    except subprocess.TimeoutExpired:
        logger.error("Timeout ao executar o reboot.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao executar o reboot (código {e.returncode}): {e.stderr}")
    except Exception as e:
        logger.error(f"Erro inesperado ao tentar reiniciar: {e}")