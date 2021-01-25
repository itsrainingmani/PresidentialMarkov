import os
from pprint import pprint

SPEECHES = './speeches'

def process_folder():
  """Process all the speeches in the speech folder"""

  for s in os.scandir(SPEECHES):
    print(s.path)
    process_file(s.path)

def process_file(path_to_file):
  pr = []
  # file_path = os.path.join(os.getcwd(), SPEECHES, path_to_file)
  with open(path_to_file, 'r') as speech:
    s = speech.read().splitlines()
    pr = [i.strip() for i in s]
    # print(type(s))
    # second_line = s[1].strip()
    # pprint(second_line)

  with open(path_to_file, 'w') as speech:
    speech.write('\n'.join(pr))
    print(f"Wrote to {path_to_file}")