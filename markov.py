#! /usr/bin/python

from collections import Counter, defaultdict
from random import randrange, randint
import re

###
# count :: Int
# word, wordn :: String
# corpus :: [String]

# countDict :: {wordn : count , wordn : count , wordn : count},...}
# wordcountTuples :: [(wordn, count)]
# nestedDict :: {wordsn-1 : countDict}
###


### Write to nestedDict ###

# Make list of words in text, lowercased
# file -> corpus :: [String]
def wordsFromCorpus(f):
  # Open the file, read it into memory as a single string.
  with open(f) as text:
    text = text.read()
  # make lower, only keep actual words, no puncutation
  return re.split("[^\w']+", text.lower())

# corpus, n -> nestedDict
def ngramsFromCorpus(corpus, n):
  # if nothing yet on the first level, makes new defaultdict (default value 0)
  nestedDict = defaultdict(lambda: defaultdict(int)) # int() === lambda: 0
  for i in range(len(corpus)-n+1):
    indexNextWord = i + n - 1 #for n == 1, returns [] 
    searchWords = ' '.join(corpus[i : indexNextWord])
    nextWord = corpus[indexNextWord]
    nestedDict[searchWords][nextWord]+=1
  return nestedDict

# dictToPartialSums :: countDict -> wordcountTuples
def dictToPartialSums(d):
  '''eg: {'crawled': 3, 'cried': 4, 'sat':2} 
  -> [('crawled', 3), ('cried', 4), ('sat',2)]'''
  lst = []
  partialSum = 0
  for k, v in d.iteritems():
    partialSum += v
    lst += [(k, partialSum)]
  return lst

# nestedDictToTuples :: nestedDict -> {String : wordcountTuples}  
## needs dictToPartialSums()
def nestedDictToTuples(d):
  ''' eg: {'cat': {'sat':2,'ate':1,'pooped':1},'baby':{'cried':4, 'crawled':3}}
  -> {'cat' : [('sat', 2),...} '''
  d_tuples = {}
  for k, v in d.iteritems():
    d_tuples[k] = dictToPartialSums(v)
  return d_tuples

# sampleNgrams :: wordcountTuples -> word 
def sampleNgrams(wordcountTuples):
  rand = randrange(wordcountTuples[-1][1])
  for i in range(len(wordcountTuples)): 
    if rand <= wordcountTuples[i][1]:
      chosenWord = wordcountTuples[i][0]
      break
  return chosenWord


### if there's no n-gram match during synthesis you try fewer-grams
# # corpus, n 
# # -> unigrams :: nestedDict 
# # -> unigramTuples :: {String : wordcountTuples}
# # -> word
# def chooseFirstWords(corpus,n):
#   unigrams = nestedDictToTuples(ngramsFromCorpus(corpus,1))
#   randIndex = randrange(len(unigrams['']))
#   firstWord =  unigrams[''][randIndex][0]
###

"""
just choose a single n
and then choose a random one to start
then from the current generatedtext
take last n-1 words
to search in dict of tuples for next one
then you have to generate random number
and find match in partial sums list
"""

""" 
you look to see if you have some ngrams with the same first n-1 
words as the previous n-1 words in your output
like if the output so far is "This is an", 
and you're doing 3-grams, you'd look for examples of "is an ___"
"""

def main():

  corpus = wordsFromCorpus('alice_in_wonderland.txt')
  
  trigrams = ngramsFromCorpus(corpus,3)

  d = nestedDictToTuples(trigrams)

  chooseFirstWords()


  print "Nested dict of tuples: "
  print unigrams
  print word


if __name__ == '__main__':
  main()
