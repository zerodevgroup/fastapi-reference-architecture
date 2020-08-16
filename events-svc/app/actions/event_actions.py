import aiohttp
import asyncio
import base64
import os
from events import EventIn, EventOut, EventUpdate
from fastapi.logger import logger
from db import events, database

STRIPE_CHARGES_URL = os.getenv("STRIPE_CHARGES_URL")
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")

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

async def add_stripe_payment(payload: PaymentIn):
    logger.debug(f"Service: Adding stripe payment with {payload}")

    # Convert amount to stripe (implied decimals)
    stripeAmount = int(payload.amount * 100)

    stripe_payload = {
        "amount": stripeAmount,
        "currency": payload.currency,
        "source": payload.source,
        "description": payload.description,
    }

    authorizationToken = base64.b64encode(f"{STRIPE_API_KEY}:".encode())

    headers = {"Authorization": "Basic " + "".join(chr(x) for x in authorizationToken)}

    async with aiohttp.ClientSession() as session:
        async with session.post(STRIPE_CHARGES_URL, data=stripe_payload, headers=headers) as resp:
            return await resp.text()
