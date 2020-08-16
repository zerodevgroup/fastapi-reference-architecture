from fastapi import FastAPI
import uvicorn

from app.constants.env_constants import LOG_LEVEL, PORT
from app.database.db import metadata, database, engine
from app.routes import router

metadata.create_all(engine)

app = FastAPI(docs_url="/_docs/", redoc_url=None)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(router, prefix='/events', tags=['events'])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True, log_level=LOG_LEVEL)
