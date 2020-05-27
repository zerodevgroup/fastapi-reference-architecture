from fastapi import FastAPI
import events_router
from db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(docs_url="/events_docs/", redoc_url=None)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(events_router.router, prefix='/events', tags=['events'])
