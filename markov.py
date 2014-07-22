#! /usr/bin/python

from collections import Counter, defaultdict
from random import randrange, choice, uniform
import re

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
def testSampleNgrams(n, wordcountTuples):
  # initialize counts
  counts = []
  for i in xrange(len(wordcountTuples)):
    counts += [0]
  for i in xrange(n):
    w = sampleNgrams(wordcountTuples)
    for i in xrange(len(wordcountTuples)):
      if w == wordcountTuples[i][0]:
        counts[i] += 1
  return counts

# testSample :: 
# (test times :: Int), (probabilities | sum to 1 :: [Float])
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


# sample :: (probabilities | sum to 1 :: [Float])
# -> (index of probability selected :: Int) 
def sample(probabilities):
  totals = [sum(probabilities[:i+1]) for i in range(len(probabilities))]
  n = uniform(0, totals[-1])
  for i, total in enumerate(totals):
      if n <= total:
          return i

# {cat: [(ate, 3), (sat, 5)], dog: [(ran,4),(jumped, 5)]}
# {my cat: [(ate, 3), (sat, 5)], his dog: [(ran,2),(jumped, 7)]}
# -> {2: {cat: [(ate, 3), (sat, 5)], dog: [(ran,4),(jumped, 5)]},
#     3: {my cat: [(ate, 3), (sat, 5)], his dog: [(ran,2),(jumped, 7)]}}

# pass in however many, but start with bigrams and go in order
## QUESTION: should totalNgrams be a list??
# bigrams, trigrams
# -> ngrams :: {2: bigrams, 3: trigrams}
# def mixNgrams(*ngrams):
#   totalNgrams = {}
#   for i in range(len(ngrams)):
#     totalNgrams[i+2] = ngrams[i]
#   return totalNgrams

# pick 2, 3, etc. with some weightings; then sample ngrams from within that
def mixMarkov(*ngrams):
  # bigrams, trigrams -> totalNgrams :: {2: bigrams, 3: trigrams} 
  totalNgrams = {}
  for i in range(len(ngrams)):
    totalNgrams[i+2] = ngrams[i]

  # pick n with some weightings
  sample

  # call markov

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
    chain += [sampleNgrams(ngrams[priorWords])] # ngrams[priorWords] :: wordcountTuples

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

def main():

  corpus = wordsFromCorpus('alice_in_wonderland.txt')
  
  bigrams   = nestedDictToTuples(ngramsFromCorpus(corpus,2))
  trigrams  = nestedDictToTuples(ngramsFromCorpus(corpus,3))
  quadgrams = nestedDictToTuples(ngramsFromCorpus(corpus,4))

  chain = markov(trigrams, 20)
  line = ' '.join(chain)
  print line

  ngrams = mixNgrams(bigrams,trigrams,quadgrams)

if __name__ == '__main__':
  main()