import subprocess
import logging
from telegram import Update
from telegram.ext import ContextTypes
from handlers.base import authorized_only
from utils.chat_cleaner import schedule_delete

logger = logging.getLogger(__name__)

@authorized_only
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Master ativo. Use /help")

@authorized_only
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "/status_dexyln – estado do bot Dexyln\n"
        "/restart_dexyln – reinicia o bot Dexyln\n"
        "/logs_dexyln – logs do bot Dexyln\n"
        "/reboot – reinicia o servidor (imediato)\n"
        "/help – ajuda"
    )
    await update.message.reply_text(texto)

@authorized_only
async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reboot imediato (sem atraso)."""
    await update.message.reply_text("🔄 A reiniciar o servidor agora...")
    subprocess.run(["/usr/bin/sudo", "/usr/local/bin/reboot_server.sh"])

async def execute_reboot(job):
    chat_id = job.context["chat_id"]
    try:
        logger.info(f"Tentando reiniciar o servidor após comando do chat {chat_id}")
        # Usa subprocess com lista de argumentos (mais seguro) e caminho absoluto
        subprocess.run(["/usr/bin/sudo", "/usr/sbin/reboot"], check=True, timeout=10)
        logger.info("Comando reboot executado com sucesso.")
    except subprocess.TimeoutExpired:
        logger.error("Timeout ao executar o reboot.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao executar o reboot (código {e.returncode}): {e.stderr}")
    except Exception as e:
        logger.error(f"Erro inesperado ao tentar reiniciar: {e}")