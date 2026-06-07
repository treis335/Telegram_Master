from telegram import Update
from telegram.ext import ContextTypes
from handlers.base import authorized_only
from utils.shell import run_cmd

@authorized_only
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    output = run_cmd("systemctl status arb_bot_dexyln --no-pager -l")
    # Limitar tamanho
    if len(output) > 4000:
        output = output[-4000:]
    await update.message.reply_text(f"📊 Estado do bot arbitragem:\n<pre>{output}</pre>", parse_mode="HTML")

@authorized_only
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 A reiniciar arb_bot_dexyln...")
    run_cmd("sudo systemctl restart arb_bot_dexyln")
    await update.message.reply_text("✅ Comando enviado. Aguarde alguns segundos e use /status_arb para verificar.")

@authorized_only
async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    output = run_cmd("journalctl -u arb_bot_dexyln -n 40 --no-pager")
    if len(output) > 4000:
        output = output[-4000:]
    await update.message.reply_text(f"📜 Últimos logs:\n<pre>{output}</pre>", parse_mode="HTML")