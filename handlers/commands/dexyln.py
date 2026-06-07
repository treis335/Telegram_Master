from telegram import Update
from telegram.ext import ContextTypes
from handlers.base import authorized_only
from utils.shell import run_cmd
from utils.chat_cleaner import schedule_delete

# Constante para tempo de auto‑apagar (2 minutos = 120 segundos)
DELETE_DELAY = 120

@authorized_only
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    output = run_cmd("systemctl status arb_bot_dexyln --no-pager -l")
    if len(output) > 4000:
        output = output[-4000:]
    msg = await update.message.reply_text(f"📊 Estado do bot Dexyln:\n<pre>{output}</pre>", parse_mode="HTML")
    # Apaga a mensagem do bot e a original após DELETE_DELAY segundos
    schedule_delete(context, update.effective_chat.id, msg.message_id, DELETE_DELAY)
    schedule_delete(context, update.effective_chat.id, update.message.message_id, DELETE_DELAY)

@authorized_only
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("🔄 A reiniciar o serviço arb_bot_dexyln...")
    schedule_delete(context, update.effective_chat.id, msg.message_id, DELETE_DELAY)
    schedule_delete(context, update.effective_chat.id, update.message.message_id, DELETE_DELAY)
    run_cmd("sudo systemctl restart arb_bot_dexyln")
    # Aguarda 2 segundos e envia confirmação (que também será apagada)
    import asyncio
    await asyncio.sleep(2)
    status_output = run_cmd("systemctl status arb_bot_dexyln --no-pager -l")
    if len(status_output) > 4000:
        status_output = status_output[-4000:]
    confirm_msg = await update.message.reply_text(f"✅ Reinício concluído.\n{status_output}", parse_mode="HTML")
    schedule_delete(context, update.effective_chat.id, confirm_msg.message_id, DELETE_DELAY)

@authorized_only
async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    output = run_cmd("journalctl -u arb_bot_dexyln -n 40 --no-pager")
    if len(output) > 4000:
        output = output[-4000:]
    msg = await update.message.reply_text(f"📜 Últimos logs do Dexyln:\n<pre>{output}</pre>", parse_mode="HTML")
    schedule_delete(context, update.effective_chat.id, msg.message_id, DELETE_DELAY)
    schedule_delete(context, update.effective_chat.id, update.message.message_id, DELETE_DELAY)