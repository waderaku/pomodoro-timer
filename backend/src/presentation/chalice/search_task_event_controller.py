from datetime import date

from src.presentation.http.response.fetch_event_response import EventTask
from fastapi import Header


async def search_event_task(
    taskId: str, lowerDate: date, upperDate: date, userId: str = Header(None)
) -> list[EventTask]:
    pass
