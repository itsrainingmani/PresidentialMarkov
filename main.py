import speech
from pprint import pprint

# asyncio.run(speech.download_all_speeches())

# speech.process_folder()

# all_speeches = speech.load_speeches()
# print(len(all_speeches))

longest_sp = speech.find_longest_speech()[0]
print("Longest Speech is " + longest_sp.split("/")[2])

speech = ""

with open(longest_sp, 'r') as f:
  speech = f.read()
  # print(speech)

speech = speech.replace('\n',' ')
speech = speech.replace('\t',' ')
speech = speech.replace('“', ' " ')
speech = speech.replace('”', ' " ')
for spaced in ['.','-',',','!','?','(','—',')']:
    speech = speech.replace(spaced, ' {0} '.format(spaced))
print(len(speech))