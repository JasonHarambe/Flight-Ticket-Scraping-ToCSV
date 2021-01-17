import requests
import time
from datetime import timedelta, date, datetime
import pandas as pd
from utils import get_lowest, daterange, post_req, run_all

def get_flight(): 
  depart_Air = input("Departing Airport? e.g. (IATA) MYY / KUL / SBW: ")
  
  depAir = str(depart_Air).upper()
  if len(depAir) != 3 or not depAir.isalpha():
    print('Departing airport is of incorrect length or non-alphabet')
    return False
  
  arrival_Air = input("Arriving Airport? e.g (without space) MYY,KUL,SBW: ")
  arrAir = arrival_Air.split(',')
  for i in arrAir:
    if len(i) != 3 or not i.isalpha():
      print('Arriving airport is of incorrect length or non-alphabet')
      return False

    i.upper()

  print(arrAir)

  depart_Date = input("Departing Date? e.g. 2021-01-27: ")
  try:
    depDate = datetime.strptime(depart_Date, '%Y-%m-%d')
  except:
    print('Date format wrong')
    return False

  arrival_Date = input("Arriving Date? e.g. 2020-02-21 : ")
  try:
    arrDate = datetime.strptime(arrival_Date, '%Y-%m-%d')
  except:
    print('Date format wrong')
    return False
  
  if arrival_Date < depart_Date:
    print('Arrival date is before departing date')
    return False

  df = run_all(
    depAir, 
    depDate, 
    arrDate, 
    arrAir
    )
  
  df.to_csv('result.csv')
  
  return True

if __name__ == '__main__':
    get_flight()