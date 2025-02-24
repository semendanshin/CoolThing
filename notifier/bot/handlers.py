from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        'Этот бот позволяет получать уведомления о статусе системы Киберцунами. '
        'Если вы являетесь администратором, то вы будете получать уведомления в этот чат'
    )
