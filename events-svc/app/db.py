import os
from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table, create_engine, ARRAY)

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

events = Table(
    'events',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('start_time', DateTime),
)

database = Database(DATABASE_URL)
