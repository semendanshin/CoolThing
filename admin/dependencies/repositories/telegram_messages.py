from abstractions.repositories.TelegramMessagesRepositoryInterface import TelegramMessagesRepositoryInterface
from infrastructure.repositories.telegram.pyrogram import PyrogramTelegramMessagesRepository


def get_telegram_messages_repository() -> TelegramMessagesRepositoryInterface:
    return PyrogramTelegramMessagesRepository()
