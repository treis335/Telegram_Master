from telegram.ext import ContextTypes

def schedule_delete(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int, delay_seconds: int):
    context.job_queue.run_once(
        lambda job: job.context.bot.delete_message(chat_id, message_id),
        delay_seconds,
        context={"bot": context.bot, "chat_id": chat_id, "message_id": message_id}
    )