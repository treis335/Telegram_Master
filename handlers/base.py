from functools import wraps
import os
from telegram import Update
from telegram.ext import ContextTypes

AUTHORIZED_ID = int(os.getenv("AUTHORIZED_USER_ID"))

def authorized_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.effective_user.id != AUTHORIZED_ID:
            await update.message.reply_text("⛔ Acesso negado.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper