import requests
import aiohttp
import asyncio
import os

from bs4 import BeautifulSoup
# from collections import defaultdict
from pprint import pprint
from aiohttp import ClientSession

INAUG_PAGE = "https://avalon.law.yale.edu/subject_menus/inaug.asp"
BASE_URL = "https://avalon.law.yale.edu"

OBAMA_URL = "https://avalon.law.yale.edu/21st_century/obama.asp"
LINCOLN_URL = 'https://avalon.law.yale.edu/19th_century/lincoln1.asp'

def get_all_speech_links():
  PRES_TUPS = []
  r = requests.get(INAUG_PAGE)
  soup = BeautifulSoup(r.text, 'html.parser')
  for link in soup.find_all('a'):
    relative_link = link.get('href').replace('..', '')
    if "_century/" in relative_link:
      pres_name = relative_link.split('_century/')[1]
      pres_name = pres_name.replace('.asp', '') 
      
      PRES_TUPS.append((pres_name, BASE_URL + relative_link))
      pprint(PRES_TUPS)

  return PRES_TUPS

def extract_speech_from_page(response):
  soup = BeautifulSoup(response.text, 'html.parser')
  speech = ""
  
  text_prop_div = soup.find('div', class_='text-properties')

  for p in text_prop_div.find_all('p'):
    speech += p.getText().strip('\n') + "\n"

  return speech

async def get_inaug_speech_async(url, session):
  pass

async def run_program(url, session):
  """Wrapper for running program in an async manner"""

  try:
    response = await get_inaug_speech_async(url, session)
    parsed_response = extract_speech_from_page(response)
    with open('speeches/' + parsed_response[0] + '.txt', 'a') as f:
      f.write(parsed_response[1])
  except Exception as err:
    print(f"Exception occurred: {err}")
    pass

r = requests.get(LINCOLN_URL)
sp = extract_speech_from_page(r)
pprint(sp)

# async def main():
#   async with ClientSession() as session:
#     # Run awaitable objects in the aws sequence concurrently.
#     # If any awaitable in aws is a coroutine, it is automatically scheduled as a Task.
#     # If all awaitables are completed successfully, the result is an aggregate list of returned values. The order of result values corresponds to the order of awaitables in aws.
#     await asyncio.gather(*[run_program(t, session) for t in PRES_TUPS])

# asyncio.run(main)