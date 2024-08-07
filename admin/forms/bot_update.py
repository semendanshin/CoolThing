from fastapi import Form, Path

from domain.dto.worker import WorkerUpdateDTO


def update_worker_form(
        id: str = Path(..., alias="bot_id"),
        bio: str = Form(...),
        username: str = Form(...),
        app_id: str = Form(...),
        app_hash: str = Form(...),
        session_string: str = Form(...),
        proxy: str = Form(default=None),
        campaign_id: str = Form(...),
        role: str = Form(...),
        status: str = Form(default=""),
) -> WorkerUpdateDTO:
    return WorkerUpdateDTO(
        id=id,
        bio=bio,
        username=username,
        app_id=app_id,
        app_hash=app_hash,
        session_string=session_string,
        proxy=proxy,
        campaign_id=campaign_id,
        role=role,
        status="active" if status.lower() == "on" else "stopped"
    )
