import asyncio
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from handlers.base import authorized_only
from utils.shell import run_cmd
from utils.chat_cleaner import schedule_delete

# Estado da conversa
WAITING_CONFIRMATION = 1

@authorized_only
async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia o pedido de confirmação para reboot."""
    msg = await update.message.reply_text(
        "⚠️ Atenção: o servidor vai reiniciar. Tem a certeza?\n"
        "Responda com *sim* ou *não* (ou /cancel para cancelar).",
        parse_mode="Markdown"
    )
    # Apaga a mensagem de pedido após 60 segundos se não responder
    schedule_delete(context, update.effective_chat.id, msg.message_id, 60)
    return WAITING_CONFIRMATION

@authorized_only
async def reboot_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa a resposta do utilizador."""
    answer = update.message.text.strip().lower()
    chat_id = update.effective_chat.id
    user_msg_id = update.message.message_id

    # Apaga a mensagem do utilizador após 5 segundos
    schedule_delete(context, chat_id, user_msg_id, 5)

    if answer in ["sim", "s", "yes", "y"]:
        confirm_msg = await update.message.reply_text("🔄 A reiniciar o servidor em 5 segundos...")
        schedule_delete(context, chat_id, confirm_msg.message_id, 10)
        # Aguarda 5 segundos e executa o reboot (função separada para não bloquear)
        asyncio.create_task(perform_reboot(context, chat_id))
    else:
        cancel_msg = await update.message.reply_text("✅ Reboot cancelado.")
        schedule_delete(context, chat_id, cancel_msg.message_id, 10)

    return ConversationHandler.END

async def perform_reboot(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    """Executa o reboot após 5 segundos e tenta enviar uma mensagem final."""
    await asyncio.sleep(5)
    # Envia uma última mensagem (pode não chegar se o servidor desligar muito rápido)
    try:
        await context.bot.send_message(chat_id, "💤 Servidor a reiniciar...")
    except:
        pass
    # Executa o comando reboot
    run_cmd("sudo /usr/sbin/reboot")

@authorized_only
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela a operação atual."""
    await update.message.reply_text("❌ Operação cancelada.")
    return ConversationHandler.END