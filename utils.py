import requests
import time
from datetime import timedelta, date
import pandas as pd
from typing import List
# import asyncio

def get_lowest(lst):
  arr = []
  
  for item in lst:
    arr.append(item['total'])

  min_price = min(arr)

  return arr.index(min_price)

def daterange(start_date, end_date):
  for n in range(int((end_date - start_date).days)):
    yield start_date + timedelta(n)

def post_req(df, depDate, depAir, arrAir, retDate = "", numAdult = 1, numChild = 0):
    df = df
    url = 'https://next-api.airpaz.com/v1/fl/flight/livecrawl'
    monitor_url = 'https://next-api.airpaz.com/v1/fl/flight/livecrawl-monitor'

    headers = {
            'content-type': 'application/json;charset=UTF-8',
        }

    payload = {
        "depAirport": depAir,
        "arrAirport": arrAir,
        "depDate": depDate,
        "retDate": retDate,
        "adult": numAdult,
        "child": numChild,
        "infant": 0,
        "currency": "MYR"
        }

    try:
        r = requests.post(url, json = payload)
    except:
        print(f'No flight to {arrAir}')
        return False

    reqId = r.json()['result']['dep']['reqId']
    print(f'reqId: {reqId} {depAir} --> {arrAir}')

    # second post API to get flight data
    monitor = {"reqId": reqId,"timestamp":0}

    # max number of tries for a certain arrival airport
    max_try = 5
    num_try = 0

    res = requests.post(monitor_url, json=monitor)

    # if no result is returned, try for max_try number of times
    while not res.json()['result']['data']:
        time.sleep(2)
        res = requests.post(monitor_url, json=monitor)

        num_try += 1
        print(f'trying {num_try} {depAir} --> {arrAir}')

        if num_try == max_try:
            
            s = pd.Series([depAir, arrAir, str(depDate), 0, 'NONE', 'NONE', 'NONE', 'NONE'], 
                index = ['Departing Airport', 'Arrival Airport', 'Date', 'Price', 'Flight Type', 'Airplane Code', 'Depart Time', 'Arrival Time'])

            df = df.append(s, ignore_index = True)

            print(f'No result found for {depAir} --> {arrAir} on {depDate}. Tried {max_try} times.')
            return df 

    flight_data = res.json()['result']['data']

    # get lowest price
    low_price_index = get_lowest(flight_data)
    price = flight_data[low_price_index]['total']
    print(f'{depAir} --> {arrAir} on {depDate}: {price}')

    #appending lowest price detail to df
    s = pd.Series([depAir, arrAir, str(depDate), int(price), flight_data[low_price_index]['type'], flight_data[low_price_index]['code'], flight_data[low_price_index]['depDateTime'], flight_data[low_price_index]['arrDateTime']], 
                index = ['Departing Airport', 'Arrival Airport', 'Date', 'Price', 'Flight Type', 'Airplane Code', 'Depart Time', 'Arrival Time'])

    df = df.append(s, ignore_index = True)

    return df

def run_all(departAirport: str, startDate: date, endDate: date, arrivalAirport: List[str]):
  df = pd.DataFrame(columns = ['Departing Airport', 'Arrival Airport', 'Date', 'Price', 'Flight Type', 'Airplane Code', 'Depart Time', 'Arrival Time'])
  lst = arrivalAirport

  start_date = startDate
  end_date = endDate
  depAirport = departAirport

  for i in range(len(lst)):
    if lst[i] == depAirport:
      print(f'Skipped {depAirport} --> {lst[i]}')
      continue
    else:
      for single_date in daterange(start_date, end_date):
        try:
            df = post_req(
                df = df,
                depDate = single_date.strftime("%Y-%m-%d"),
                depAir = depAirport,
                arrAir = str(lst[i])
            )
        except:
            print(f'Exception raised for {depAirport} --> {lst[i]} on {startDate}')
            pass

  return df