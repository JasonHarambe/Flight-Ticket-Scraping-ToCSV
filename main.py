import requests
import time
from datetime import timedelta, date
import pandas as pd
from utils import get_lowest, daterange, post_req, run_all

#FastAPI
from typing import Optional
from fastapi import FastAPI
from model import Flight

app = FastAPI()

@app.get("/")
def home():
  return {"Home": "True"}

@app.post('/flight/')
def get_flight(flight: Flight):
  flight_data = flight.dict()
  
  df = run_all(
    flight.departAirport, 
    flight.departDate, 
    flight.arrivalDate, 
    flight.arrivalAirport
    )
  
  res = df.to_dict()

  return res