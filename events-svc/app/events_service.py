from events import EventIn, EventOut, EventUpdate
from fastapi.logger import logger
from db import events, database

async def add_event(payload: EventIn):
    logger.debug(f"Service: Adding event with {payload}")
    query = events.insert().values(**payload.dict())
    return await database.execute(query=query)

async def get_all_events():
    logger.debug(f"Service: Getting all events")
    query = events.select()
    return await database.fetch_all(query=query)

async def get_event(id):
    logger.debug(f"Service: Getting event {id}")
    query = events.select(events.c.id==id)
    return await database.fetch_one(query=query)

async def delete_event(id: int):
    logger.debug(f"Service: Deleting event {id}")
    query = events.delete().where(events.c.id==id)
    return await database.execute(query=query)

async def update_event(id: int, payload: EventIn):
    logger.debug(f"Service: Updating event {id} with {payload}")
    query = (
        events
        .update()
        .where(events.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)
