from pydantic import BaseModel
from datetime import timedelta, date
from typing import List

class Flight(BaseModel):
    departAirport: str
    arrivalAirport: List[str]
    departDate: date
    arrivalDate: date