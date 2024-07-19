import asyncio

from pydantic_settings import BaseSettings, SettingsConfigDict
from telegram import Update, InlineKeyboardButton, WebAppInfo, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler


class Settings(BaseSettings):
    tg_bot_token: str
    host: str

    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    webapp = WebAppInfo(
        url=f"{settings.host}/dashboard",
        api_kwargs={"headers": {"ngrok-skip-browser-warning": "true"}},
    )
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Открыть приложение", web_app=webapp),
            ]
        ]
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Админ-панель тут:",
        reply_markup=keyboard,
    )


def main():
    app = Application.builder().token(settings.tg_bot_token).build()

    app.add_handler(
        CommandHandler(
            command="start",
            callback=start,
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
