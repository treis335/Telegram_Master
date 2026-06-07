import asyncio
from telegram import Bot
from telegram.ext import ContextTypes

async def delete_message_after_delay(bot: Bot, chat_id: int, message_id: int, delay_seconds: int):
    """Apaga uma mensagem após X segundos (chamada assíncrona)."""
    await asyncio.sleep(delay_seconds)
    try:
        await bot.delete_message(chat_id, message_id)
    except Exception:
        pass  # ignora erros (mensagem já apagada, sem permissão, etc.)

def schedule_delete(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int, delay_seconds: int):
    """
    Agenda a eliminação de uma mensagem usando a JobQueue do context.
    Uso: schedule_delete(context, chat_id, message_id, 120)
    """
    context.job_queue.run_once(
        lambda job: job.context.bot.delete_message(job.context.chat_id, job.context.message_id),
        delay_seconds,
        context={"bot": context.bot, "chat_id": chat_id, "message_id": message_id}
    )