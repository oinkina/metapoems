#! /usr/bin/python

from collections import Counter, defaultdict
from random import randrange, choice, uniform
import re

import json

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


### Tests of Probability Samplings ###

# test sampling of wordcountTuples
def testSampleWords(n, wordcountTuples):
  # initialize counts
  counts = []
  for i in xrange(len(wordcountTuples)):
    counts += [0]
  for i in xrange(n):
    w = sampleWords(wordcountTuples)
    for i in xrange(len(wordcountTuples)):
      if w == wordcountTuples[i][0]:
        counts[i] += 1
  return counts

# testSample :: 
# (test times :: Int), (probabilities :: Float || Int)
#   -> (counts in n trials :: [Int])
def testSample(n, probabilities):

  # initialize counts
  counts = []
  for i in xrange(len(probabilities)):
    counts += [0]

  for i in xrange(n):
    choice = sample(probabilities)
    counts[choice] += 1

  return counts

#####


### TYPES ###

# count :: Int
# word, wordn :: String
# corpus :: [String]

# countDict :: {wordn : count , wordn : count , wordn : count},...}
# wordcountTuples :: [(wordn, count)]
# nestedDict :: {wordsn-1 : countDict}

#####



### Write to nestedDict ###

# Make list of words in text, lowercased
# file -> corpus :: [String]
def wordsFromCorpus(f):
  # Open the file, read it into memory as a single string.
  with open(f) as text:
    text = text.read()

#change opening it from file to opening it from url

  # with urllib2.urlopen(f) as text:
  #   text = text.read()

  # make lower, only keep actual words, no puncutation
  return re.split("[^\w']+", text.lower())

# (corpus :: [Words]), maxN -> (nestedDict :: {bigrams, trigrams, ...})
def ngramsFromCorpus(corpus, maxN):
  # if nothing yet on the first level, makes new defaultdict (default value 0)
  nestedDict = defaultdict(lambda: defaultdict(int)) # int() === lambda: 0
  # for bigrams, trigrams, etc through maxN-grams
  for n in range(2, maxN + 1):
    # for all words in corpus, count++ in nestedDict[wordsn-1] = {wordn: count} 
    for i in range(len(corpus)-n+1):
      indexNextWord = i + n - 1 #for n == 1, returns [] 
      searchWords = ' '.join(corpus[i : indexNextWord])
      nextWord = corpus[indexNextWord]
      nestedDict[searchWords][nextWord] += 1
  return nestedDict

# dictToPartialSums :: countDict -> wordcountTuples
def dictToPartialSums(d):
  '''eg: {'crawled': 3, 'cried': 4, 'sat':2} 
  -> [('crawled', 3), ('cried', 7), ('sat',9)]'''
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

# sampleWords :: wordcountTuples -> word 
def sampleWords(wordcountTuples):
  rand = randrange(wordcountTuples[-1][1])
  for i in range(len(wordcountTuples)): 
    if rand < wordcountTuples[i][1]:
      chosenWord = wordcountTuples[i][0]
      break
  return chosenWord

# sample :: (probabilities :: Float || Int)
# -> (index of probability selected :: Int) 
def sample(probabilities):
  totals = [sum(probabilities[:i+1]) for i in range(len(probabilities))]
  n = uniform(0, totals[-1])
  for i, total in enumerate(totals):
      if n <= total:
          return i

# note: probabilities are in order for bigrams, trigrams, etc.; sum to 1; len == (maxN - 1)
# (ngrams :: {String : wordcountTuples}), (lineLength :: Int), 
# (n_probabilities :: [P(n-gram) :: Float])
# -> firstNgram :: String
# -> line :: String
# def markov(ngrams, lineLength, lines, n_probabilities=[0.5,0.5]):
#   ## note: underweights ngrams with lots of instances for first word
#   firstNgram = choice(ngrams.items()) # :: (wordn-1, [(wordn, count)])
#   firstStr = firstNgram[0] + " " + choice(firstNgram[1])[0] # :: "wordn-1 wordn"
#   chain = firstStr.split(' ') # :: [wordn-1, wordn]

#   for i in xrange(lineLength-len(chain)):
#     n = sample(n_probabilities)+2 
#     priorWords = ' '.join(chain[-n+1:]) # take last n-1 words to end of chain
#     chain += [sampleWords(ngrams[priorWords])] # ngrams[priorWords] :: wordcountTuples

#   return chain

# (n :: Int), (chain :: [Word]), ngrams -> Word
def sampleNgrams(n, chain, ngrams):
  priorWords = ' '.join(chain[-n+1:]) # take last n-1 words to end of chain
  if priorWords in ngrams:
    return [sampleWords(ngrams[priorWords])]
  elif n > 0: 
      return sampleNgrams(n - 1, chain, ngrams)
  else:
      return firstWords(ngrams)

# ngrams -> [Word]
def firstWords(ngrams):
  ## note: underweights ngrams with lots of instances for first word
  firstNgram = choice(ngrams.items()) # :: (wordn-1, [(wordn, count)])
  firstStr = firstNgram[0] + " " + choice(firstNgram[1])[0] # :: "wordn-1 wordn"
  return firstStr.split(' ') # :: [wordn-1, wordn]

def markov(ngrams, lineLength, error, lines, n_probabilities=[0.5,0.5]):
  chain = firstWords(ngrams)
  currentLineLength = len(chain)
  poem = chain[:]
  linesCount = lines

  # for each line
  while linesCount > 0:
    thisLineLength = abs(lineLength + randrange(-1*error, error))
    # for each word in line
    while currentLineLength < thisLineLength:
      n = sample(n_probabilities)+2 
      nextWord = sampleNgrams(n, chain, ngrams)
      poem += nextWord
      chain += nextWord
      currentLineLength += 1

    poem += [" <br> "]
    currentLineLength = 0
    if linesCount == lines:
      title = poem
      for i in range(-len(title)):
        poem.pop(i)
    linesCount -= 1

  return (title, poem)


# TODOs:
# <s> </s> tags for reasonable starts and ends
## turn periods into </s>, <s>
## chain starts with n-1 <s>'s, then can select from ngrams: 
  ### start tags:
  ### {'ANYTHING <s>...':[('blah',3), (blah2, 4)]} -- as long as has <s> as last word in key 
  ### "alice went to bed. the next morning" -> {"bed </s> <s>" : [(next, 4)]}
  ### end tags:
  ### "alice went to bed" {"went to bed" : [(</s>:10, "today":1)]} -> choose </s>
  ### if select next word that is an </s>, add period and start new sentence with "wordsn-1 </s> <s>""
# TODO!!: default to smaller ngrams if no ngrams exist for that n; 
  # choose random next word if nothing for bigrams
## weight different ngrams (2,3,4) -- learn weights?
# rhyming


def generatePoem(corpus, lineLength=5, error = 0, lines=20, weights=[0.1,0.7,0.2]):
  corp = wordsFromCorpus(corpus)
  ngrams = nestedDictToTuples(ngramsFromCorpus(corp, 4))
  title, poem = markov(ngrams, lineLength, error, lines, weights)
  return (' '.join(title), ' '.join(poem))




def main():
  corpus = 'corpus/poe.txt'
  print generatePoem(corpus, 7, 3, 10)

if __name__ == '__main__':
  main()


