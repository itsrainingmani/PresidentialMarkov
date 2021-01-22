import os

SPEECHES = './speeches'

def process_folder():
  for s in os.scandir(SPEECHES):
    print(s.path)
    processed_speech = ''
    with open(s.path, 'r+') as speech:
      for line in speech:
        processed_speech += line.strip() + '\n'
      print(f"Writing to {s.path.split('/')[2]}\n")
      speech.write(processed_speech)