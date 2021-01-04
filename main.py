import requests
import time
from datetime import timedelta, date
import pandas as pd

# defining df to store flight details
df = pd.DataFrame(columns = ['Departing Airport', 'Arrival Airport', 'Date', 'Price'])

lst = ['BTU','BLG','LSM','LGL','KCH','ODN','LMN','MKM','LKH','MUR','BSE','KPI','BKM','MYY','SBW','TGC','LSU','LWY','SGG','BBN','SMM','LDU','TEL','KGU','SXS','BKI','LBU','TMG','GSA','SPE','PAY','RNU','SDK','KUD','TWU','MZV','SXT','MEP','SWY','TPG','TOD','AOR','BWH','KBR','KUA','KTE','IPH','JHB','KUL','LGK','MKZ','TGG','PEN','PKG','RDN','SZB']

# api call return a list of flight. Get the lowest price from the list.
def get_lowest(lst):
  arr = []
  for item in lst:
    arr.append(item['total'])
  return min(arr)

def post_req(depDate, depAir, arrAir, retDate = "", numAdult = 1, numChild = 0):
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
  
  # first post API to get a reqID.
  try:
    r = requests.post(url, json = payload)
  except:
    print(f'No flight to {arrAir}')
    return False

  reqId = r.json()['result']['dep']['reqId']
  print(f'reqId: {reqId}')

  # second post API to get flight data
  monitor = {"reqId": reqId,"timestamp":0}

  # max number of tries for a certain arrival airport
  max_try = 15
  num_try = 0

  res = requests.post(monitor_url, json=monitor)

  # if no result is returned, try for max_try number of times
  while not res.json()['result']['data']:
    time.sleep(2)
    res = requests.post(monitor_url, json=monitor)

    num_try += 1
    print(f'trying {num_try} {arrAir}')

    if num_try == max_try:
      print(f'No Request Found {arrAir} on {depDate}')
      return False 
  
  flight_data = res.json()['result']['data']
  
  # get lowest price
  low_price = get_lowest(flight_data)

  print(f'{depAir}, {arrAir}, {depDate}, {low_price} DONE')

  #appending lowest price detail to df
  s = pd.Series([depAir, arrAir, str(depDate), int(low_price)], index = ['Departing Airport', 'Arrival Airport', 'Date', 'Price'])
  
  global df
  df = df.append(s, ignore_index = True)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2021, 3, 1) #change this
end_date = date(2021, 4, 1) #change this
depAirport = 'MYY' #change this

# lst could be multiple arrival airport 
for i in range(len(lst)):
  if lst[i] == depAirport:
    print(f'Skipped {lst[i]}')
    pass
  else:
    for single_date in daterange(start_date, end_date):
      try:
        post_req(
            depDate = single_date.strftime("%Y-%m-%d"),
            depAir = depAirport,
            arrAir = str(lst[i])
        )
      except:
        pass

df.to_csv('data.csv')