#! /usr/bin/python

from collections import Counter, defaultdict
from random import randrange, choice
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

# sampleNgrams :: wordcountTuples -> word 
def sampleNgrams(wordcountTuples):
  rand = randrange(wordcountTuples[-1][1])
  for i in range(len(wordcountTuples)): 
    if rand < wordcountTuples[i][1]:
      chosenWord = wordcountTuples[i][0]
      break
  return chosenWord

# test sampling of sampleNgrams
# def testProbs(n, wordcountTuples):
#   counts = []
#   for i in xrange(len(wordcountTuples)):
#     counts += [0]
#   for i in xrange(n):
#     w = sampleNgrams(wordcountTuples)
#     for i in xrange(len(wordcountTuples)):
#       if w == wordcountTuples[i][0]:
#         counts[i] += 1
#   return counts


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

# ngrams :: {String : wordcountTuples} 
# -> firstNgram :: String
# -> line :: String
def markov(ngrams, lineLength):
  ## note: underweights ngrams with lots of instances for first word
  firstNgram = choice(ngrams.items()) # :: (wordn-1, [(wordn, count)])
  firstStr = firstNgram[0] + " " + choice(firstNgram[1])[0] # :: "wordn-1 wordn"
  chain = firstStr.split(' ') # :: [wordn-1, wordn]

  n = len(chain)
  for i in xrange(lineLength-n):
    priorWords = ' '.join(chain[-n+1:]) # take last n-1 words to end of chain
    chain += [ngrams[priorWords][0][0]]

  return chain


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
# default to smaller ngrams if no ngrams exist for that n
## weight different ngrams (2,3,4) -- learn weights?
# rhyming

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

  chain = markov(d, 20)

  line = ' '.join(chain)

  print line

if __name__ == '__main__':
  main()
