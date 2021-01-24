import os
from pprint import pprint

SPEECHES = './speeches'

def process_folder():
  """Process all the speeches in the speech folder"""

  for s in os.scandir(SPEECHES):
    print(s.path)
    processed_speech = ''
    with open(s.path, 'r+') as speech:
      for line in speech:
        processed_speech += line.strip() + '\n'
      print(f"Writing to {s.path.split('/')[2]}\n")
      speech.write(processed_speech)

def process_file(filename):
  pr = []
  file_path = os.path.join(os.getcwd(), SPEECHES, filename)
  with open(file_path, 'r') as speech:
    s = speech.read().splitlines()
    pr = [i.strip() for i in s]
    # print(type(s))
    # second_line = s[1].strip()
    # pprint(second_line)

  with open(file_path, 'w') as speech:
    speech.write('\n'.join(pr))
    print(f"Wrote to {filename}")