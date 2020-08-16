from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.logger import logger

from events import EventIn, EventOut, EventUpdate
import events_controller

router = APIRouter()

@router.post('/', response_model=EventOut, status_code=201)
async def create_event(payload: EventIn):
    event_id = await events_controller.add_event(payload)
    response = {
        'id': event_id,
        **payload.dict()
    }

    return response

@router.get("/", response_model=List[EventOut])
async def index():
    return await events_controller.get_all_events()

@router.get('/{id}/', response_model=EventOut)
async def get_event(id: int):
    event = await events_controller.get_event(id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put('/{id}/', response_model=EventOut)
async def update_event(id: int, payload: EventUpdate):
    event = await events_controller.get_event(id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    update_data = payload.dict(exclude_unset=True)

    event_in_db = EventIn(**event)

    updated_event = event_in_db.copy(update=update_data)

    return await events_controller.update_event(id, updated_event)

@router.delete('/{id}/', response_model=None)
async def delete_event(id: int):
    event = await events_controller.get_event(id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return await events_controller.delete_event(id)

# Stripe routes
@router.post('/stripe/', status_code=201)
async def create_stripe_payment(payload: PaymentIn):
    response = await payments_controller.add_stripe_payment(payload)
    logger.debug(f"Router: Got this from stripe payment: {response}")
    return response
