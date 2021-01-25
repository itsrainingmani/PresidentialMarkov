import requests
import aiohttp
import asyncio
import os

import speech

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

  return PRES_TUPS

def extract_speech_from_page(response_text):
  soup = BeautifulSoup(response_text, 'html.parser')
  speech = ""
  
  text_prop_div = soup.find('div', class_='text-properties')

  for p in text_prop_div.find_all('p'):
    speech += p.getText().strip('\n') + "\n"

  return speech

async def get_inaug_speech_async(url, session):
  try:
    response = await session.request(method='GET', url=url)
    response.raise_for_status()
    print(f"Response status ({url}): {response.status}")
  except Exception as err:
      print(f"An error ocurred: {err}")
  response_text = await response.text()
  return response_text
  

async def run_program(pres, session):
  """Wrapper for running program in an async manner"""
  name, url = pres

  try:
    response_text = await get_inaug_speech_async(url, session)
    parsed_response = extract_speech_from_page(response_text)
    print(f"Writing {url} to speeches/{name}.txt\n")
    with open('speeches/' + name + '.txt', 'a') as f:
      f.write(parsed_response)
  except Exception as err:
    print(f"Exception occurred: {err}")
    pass

# r = requests.get(LINCOLN_URL)
# sp = extract_speech_from_page(r)
# pprint(sp)

async def main():
  async with ClientSession() as session:
    # Run awaitable objects in the aws sequence concurrently.
    # If any awaitable in aws is a coroutine, it is automatically scheduled as a Task.
    # If all awaitables are completed successfully, the result is an aggregate list of returned values. The order of result values corresponds to the order of awaitables in aws.
    await asyncio.gather(*[run_program(t, session) for t in get_all_speech_links()])

# asyncio.run(main())

speech.process_folder()
# speech.process_file('bush.txt')