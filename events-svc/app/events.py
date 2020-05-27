from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class EventIn(BaseModel):
    name: str
    start_time: datetime
    end_time: datetime

class EventOut(EventIn):
    id: int

class EventUpdate(EventIn):
    name: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
