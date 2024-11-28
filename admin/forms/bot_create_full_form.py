import re

from fastapi import Form

from domain.dto.worker import WorkerCreateDTO


def bot_create_full_form(
        username: str = Form(...),
        app_id: str = Form(...),
        app_hash: str = Form(...),
        session_string: str = Form(...),
        proxy: str = Form(default=None),
        role: str = Form(...),
        status: str = Form(default=""),
        campaign_id: str = Form(default=None),
        bio: str = Form(None),
        chats: str = Form(default=""),
) -> WorkerCreateDTO:
    return WorkerCreateDTO(
        username=username,
        app_id=app_id,
        app_hash=app_hash,
        session_string=session_string,
        proxy=proxy,
        role=role,
        status="active" if status.lower() == "on" else "stopped",
        campaign_id=campaign_id if campaign_id else None,
        bio=bio,
        chats=[chat for chat in re.split(r"\s+", chats)],
    )
