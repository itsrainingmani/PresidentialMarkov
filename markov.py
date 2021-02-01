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

  corpus_words = corpus.split(' ')
  corpus_words = [word for word in corpus_words if word != '']
  print(corpus_words[:10])
  print(len(corpus_words))

  distinct_words = list(set(corpus_words))
  word_idx_dict = {word: i for i, word in enumerate(distinct_words)}

  distinct_words_count = len(list(set(corpus_words)))
  print(distinct_words_count)
