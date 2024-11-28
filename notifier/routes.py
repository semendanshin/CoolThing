import logging

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from dependencies.services.notifications import get_notification_service
from domain.events import (
    Event,
    event_factory
)

router = APIRouter(
    prefix='/events',
    tags=['Events'],
)

logger = logging.getLogger(__name__)


@router.post('')
async def new_event(
        event: Event,
        request: Request
):
    try:
        data = await request.json()
        event = event_factory(data)

        logger.info(event)
        notification_service = get_notification_service()
        await notification_service.send_notification(event=event)

        return JSONResponse(content={"status": "Event processed"}, status_code=200)
    except ValueError as e:
        logger.error(f"Invalid event data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
