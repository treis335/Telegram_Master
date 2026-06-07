from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from handlers.base import authorized_only
from utils.shell import run_cmd
from utils.chat_cleaner import schedule_delete

# Estado para o ConversationHandler do reboot
WAITING_CONFIRMATION = 1

@authorized_only
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text(
        "🤖 Bot Master ativo.\nComandos disponíveis: /help"
    )
    # Apaga a mensagem do bot após 60 segundos
    schedule_delete(context, update.effective_chat.id, msg.message_id, 60)
    # Opcional: apagar também a mensagem original do utilizador
    schedule_delete(context, update.effective_chat.id, update.message.message_id, 60)

@authorized_only
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "/status_dexyln – estado do bot de arbitragem (Dexyln)\n"
        "/restart_dexyln – reinicia o bot de arbitragem (Dexyln)\n"
        "/logs_dexyln – últimos logs do bot de arbitragem (Dexyln)\n"
        "/reboot – reinicia o servidor (com confirmação)\n"
        "/help – mostra esta ajuda\n\n"
        "Os comandos antigos /status_arb, /restart_arb, /logs_arb também funcionam.\n"
        "As mensagens são auto‑apagadas após alguns minutos."
    )
    msg = await update.message.reply_text(texto)
    schedule_delete(context, update.effective_chat.id, msg.message_id, 120)
    schedule_delete(context, update.effective_chat.id, update.message.message_id, 120)

@authorized_only
async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia o pedido de confirmação para reboot."""
    msg = await update.message.reply_text(
        "⚠️ Atenção: o servidor vai reiniciar. Tem a certeza?\n"
        "Responda com *sim* ou *não* (ou /cancel para cancelar).",
        parse_mode="Markdown"
    )
    schedule_delete(context, update.effective_chat.id, msg.message_id, 60)
    schedule_delete(context, update.effective_chat.id, update.message.message_id, 60)
    return WAITING_CONFIRMATION

@authorized_only
async def reboot_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa a resposta do utilizador."""
    answer = update.message.text.strip().lower()
    chat_id = update.effective_chat.id
    user_msg_id = update.message.message_id

    # Apaga a mensagem de resposta do utilizador
    schedule_delete(context, chat_id, user_msg_id, 10)

    if answer in ["sim", "s", "yes", "y"]:
        confirm_msg = await update.message.reply_text("🔄 A reiniciar o servidor em 5 segundos...")
        schedule_delete(context, chat_id, confirm_msg.message_id, 10)
        # Agenda o reboot com atraso (para a mensagem ser entregue)
        import asyncio
        asyncio.create_task(delayed_reboot())
    else:
        cancel_msg = await update.message.reply_text("✅ Reboot cancelado.")
        schedule_delete(context, chat_id, cancel_msg.message_id, 10)

    return ConversationHandler.END

async def delayed_reboot():
    await asyncio.sleep(5)
    run_cmd("sudo reboot")

@authorized_only
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela a operação atual (reboot)."""
    msg = await update.message.reply_text("Operação cancelada.")
    schedule_delete(context, update.effective_chat.id, msg.message_id, 10)
    schedule_delete(context, update.effective_chat.id, update.message.message_id, 10)
    return ConversationHandler.END