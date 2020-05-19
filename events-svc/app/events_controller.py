from events import EventIn, EventOut, EventUpdate
from db import events, database

async def add_event(payload: EventIn):
    query = events.insert().values(**payload.dict())
    return await database.execute(query=query)

async def get_all_events():
    query = events.select()
    return await database.fetch_all(query=query)

async def get_event(id):
    query = events.select(events.c.id==id)
    return await database.fetch_one(query=query)

async def delete_event(id: int):
    query = events.delete().where(events.c.id==id)
    return await database.execute(query=query)

async def update_event(id: int, payload: EventIn):
    query = (
        events
        .update()
        .where(events.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)
