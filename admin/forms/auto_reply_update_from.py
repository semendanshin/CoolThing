from fastapi import Form, Path

from domain.dto.chat import UpdateAutoReplyDTO


def auto_reply_update_form(
        auto_reply: str = Form(default=""),
) -> UpdateAutoReplyDTO:
    return UpdateAutoReplyDTO(
        auto_reply=True if auto_reply.lower() == "on" else False,
    )
