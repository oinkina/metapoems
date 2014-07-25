  url = "http://rhymebrain.com/talk?function=getRhymes&word=my"
  try:
    result = urllib2.urlopen(url).read()
  except urllib2.URLError, e:
    print e

  rhymesDicts = json.loads(result)

  scores = []
  words = []
  for word in rhymesDicts:
    words.append(word["word"])
    scores.append(word["score"])

  '''
  Sample from rhyming words until one of them is in the corpus. 
  Remove word each time it's picked and not in corpus
  If you run out of words, pick the one with the highest frequency (first in rhymesDicts)
  '''

  word = None
  while not word in corpus:
    index = sample(scores)
    chosenWord = words[index]
    words.remove(words[index]) 
    print "Chosen Word: %s" %chosenWord

