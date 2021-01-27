import speech
from pprint import pprint

# asyncio.run(speech.download_all_speeches())

# speech.process_folder()

all_speeches = speech.load_speeches()
print(len(all_speeches))