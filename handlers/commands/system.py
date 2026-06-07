import subprocess
import logging
from telegram import Update
from telegram.ext import ContextTypes
from handlers.base import authorized_only
from utils.chat_cleaner import schedule_delete
from utils.shell import run_cmd

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
        "/bots – lista todos os bots ativos\n"
        "/help – esta ajuda"
    )
    await update.message.reply_text(texto)

@authorized_only
async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reboot imediato (sem atraso)."""
    await update.message.reply_text("🔄 A reiniciar o servidor agora...")
    subprocess.run(["/usr/bin/sudo", "/usr/local/bin/reboot_server.sh"])

@authorized_only
async def bots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista todos os bots ativos no servidor (processos node/python do utilizador servidor)."""
    # Comando ps que já testaste
    cmd = "ps aux | grep 'servidor' | grep -E 'node|python' | grep -v 'grep' | grep -v 'telegram-master'"
    output = run_cmd(cmd)

    if not output.strip():
        await update.message.reply_text("📭 Nenhum bot ativo encontrado.")
        return

    lines = output.strip().split('\n')
    bot_list = []
    for line in lines:
        # Extrair apenas o comando (caminho do script)
        parts = line.split()
        if len(parts) >= 11:
            cmd_line = ' '.join(parts[10:])
        else:
            cmd_line = line
        bot_list.append(f"• {cmd_line}")

    resposta = f"📊 **Bots ativos no servidor** ({len(bot_list)}):\n\n" + "\n".join(bot_list)
    if len(resposta) > 4000:
        resposta = resposta[:4000] + "\n...(truncado)"

    await update.message.reply_text(resposta, parse_mode="Markdown")