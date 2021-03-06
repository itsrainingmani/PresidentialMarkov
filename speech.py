import os
import requests
import aiohttp
import asyncio

from bs4 import BeautifulSoup
# from collections import defaultdict
from pprint import pprint
from aiohttp import ClientSession

INAUG_PAGE = "https://avalon.law.yale.edu/subject_menus/inaug.asp"
BASE_URL = "https://avalon.law.yale.edu"

OBAMA_URL = "https://avalon.law.yale.edu/21st_century/obama.asp"
LINCOLN_URL = 'https://avalon.law.yale.edu/19th_century/lincoln1.asp'

SPEECHES = './speeches'

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
  print(text_prop_div)

  for p in text_prop_div.find_all('p'):
    speech += p.getText().strip('\n') + "\n"

  # print(speech[0:10])
  return speech

async def get_inaug_speech_async(url, session):
  try:
    response = await session.request(method='GET', url=url)
    response.raise_for_status()
    print(f"Response status ({url}): {response.status}")
  except Exception as err:
      print(f"An error ocurred: {err}")
  response_text = await response.text()
  # print(f"{url}\n")
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
# sp = extract_speech_from_page(r.text)
# pprint(sp)

async def download_all_speeches():
  async with ClientSession() as session:
    # Run awaitable objects in the aws sequence concurrently.
    # If any awaitable in aws is a coroutine, it is automatically scheduled as a Task.
    # If all awaitables are completed successfully, the result is an aggregate list of returned values. The order of result values corresponds to the order of awaitables in aws.
    await asyncio.gather(*[run_program(t, session) for t in get_all_speech_links()])

def process_folder():
  """Process all the speeches in the speech folder"""

  for s in os.scandir(SPEECHES):
    print(s.path)
    process_file(s.path)

def process_file(path_to_file):
  """Remove newlines and whitespace chars from the end of each line in a speech"""

  pr = []
  # file_path = os.path.join(os.getcwd(), SPEECHES, path_to_file)
  with open(path_to_file, 'r') as speech:
    s = speech.read().splitlines()
    pr = [i.strip() for i in s]

    # Construct an iterator from those elements of iterable for which function returns true
    pr = filter(lambda x: x != '', pr)

  with open(path_to_file, 'w') as speech:
    speech.write('\n'.join(pr))
    print(f"Wrote to {path_to_file}")

def load_speeches():
  """Read all speeches into a string"""

  all_speeches = ""
  for sp in os.scandir(SPEECHES):
    with open(sp.path, 'r') as f:
      speech = f.read()
      # print(len(speech))
      all_speeches += speech

  return all_speeches

def find_longest_speech():
  """Iterates through all the speeches and finds the longest one"""

  longest_sp = ""
  longest_sp_len = 0
  for sp in os.scandir(SPEECHES):
    with open(sp.path, 'r') as f:
      speech = f.read()
      if len(speech) > longest_sp_len:
        longest_sp_len = len(speech)
        longest_sp = sp.path
  
  return (longest_sp, longest_sp_len)