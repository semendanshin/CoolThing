from fastapi import Form

from domain.dto.chat import SendMessageDTO


def send_message_form(
    message: str = Form(...),
) -> SendMessageDTO:
    return SendMessageDTO(
        message=message,
)
