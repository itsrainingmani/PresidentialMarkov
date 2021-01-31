import os
import speech

def process_corpus(corpus):

  # Adds spaces on both sides of the following tokens
  corpus = corpus.replace('\n',' ')
  corpus = corpus.replace('\t',' ')
  corpus = corpus.replace('“', ' " ')
  corpus = corpus.replace('”', ' " ')
  for spaced in ['.','-',',','!','?','(','—',')']:
      corpus = corpus.replace(spaced, ' {0} '.format(spaced))
  print(len(corpus))