#!/usr/bin/python
#
# William Hartmann (hartmannw@gmail.com)
# This is free and unencumbered software released into the public domain.
# See the UNLICENSE file for more information.
#
# Given a set of hypothesied pronunciations, the script generates a set of
# likely transformations for the pronunciation dictionary.

import getopt, sys, string, re, operator, string_manip

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:p:e:s:c:f", 
        ["help", "dictionary=", "pronunciation=", "examples=", 
          "score=", "cost=", "force"])
  except getopt.GetoptError:
    usage()

  cost = {}
  force_single_word = False
  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
    if o in ("-d", "--dictionary"):
      dictfile = str(a);
    if o in ("-p", "--pronunciation"):
      hfile= str(a)
    if o in ("-e", "--examples"):
      min_examples = int(a)
    if o in ("-s", "--score"):
      min_score = float(a)
    if o in ("-c", "--cost"):
      cost = LoadCostMatrix(str(a))
    if o in ("-f", "--force"):
      force_single_word = True

  # Load in the dictionary file
  dictionary = {}
  fin = open(dictfile, "r")
  for line in fin:
    data = re.split(" ", line.strip())
    dictionary[data[0]] = data[1:]
  fin.close()

  # Count the frequencies of each transformation
  count = {}
  fin = open(hfile, "r")
  for line in fin:
    data = re.split(" ", line.strip())
    pron = dictionary[data[0]]
    distance, transform = string_manip.EditDistance(pron, data[1:], cost)
    if len(transform) >= distance:
      for i in range(len(pron)):
        sub = transform.get(str(i), pron[i])
        context = GenerateNGramSubstitutions(pron, i, sub)
        ins = transform.get(str(i) + ':' + str(i+1), '')
        context.update( GenerateNGramInsertion(pron, i, i+1, ins) )
        if i == 0: # Allows for an insertion before first phone.
          ins = transform.get(str(i-1) + ':' + str(i), '')
          context.update( GenerateNGramInsertion(pron, i-1, i, ins) )
        for k,v in context.items():
          count[k] = count.get(k,{}) # Force it to be set
          count[k][v] = count.get(k,{}).get(v,0) + 1
  fin.close()
  
  # Now to evaluate the results
  # PrintTopChoice(count, min_examples, min_score)
  rules = SelectRules(count, min_examples, min_score, force_single_word)

  # Transform original dictionary
  fin = open(dictfile, "r")
  for line in fin:
    data = re.split(" ", line.strip() )
    word = data[0]
    orig = data[1:]
    pron = TransformPronunciation(orig, rules)
    print word + pron
  fin.close()

# Assumes the file contains a confusion matrix between phones with integer 
# counts. The first line contains the total number of phones and each line
# contains a model names. The actual confusion matrix follows the list of model
# names.
def LoadCostMatrix(cfile):
  cost = {}
  fin = open(cfile, "r")
  # First line should contain the number of models
  total = int(fin.readline().strip() )
  models = []
  for i in range(total):
    models.append(fin.readline().strip() )
    cost[ models[i] ] = {}
  models.append("")
  cost[""] = {} # Add row for insertion

  for i in range(len(models)):
    line = fin.readline().strip()
    data = re.split(' ', line)
    data = [int(item) for item in data]
    total = float(sum(data)) # So that when normalizing, we get a float.
    for j in range(len(data)):
      cost[ models[i]][models[j]] = 1 - (data[j] / total)

  fin.close()
  return cost

def TransformPronunciation(orig, rules):
  pron =''
  for i in range(len(orig)):
    if i == 0: # Check if insertion before first character
      context = GenerateNGramContext(orig, i-1, i, 3)
      pron = pron + SelectTransform(context, rules, '')
    # Handle substitution or deletion
    context = GenerateNGramContext(orig, i, i, 3)
    pron = pron + SelectTransform(context, rules, orig[i])
    # Handle insertion
    context = GenerateNGramContext(orig, i, i+1, 3)
    pron = pron + SelectTransform(context, rules, '')
  return pron

def SelectTransform(context, rules, phone):
  for c in context:
    phone = rules.get(c, phone)
  if len(phone) > 0:
    phone = " " + phone
  return phone

def SelectRules(count, min_examples, min_score, force_single_word):
  rules = {}
  for k,v in count.items():
    # first get total examples
    total = 0
    for c in v.values():
      total += c
    if total >= min_examples:
      bestkey, bestvalue = max(v.iteritems(), key=operator.itemgetter(1))
      if bestkey != GetMiddle(k): # Limits size of rule set.
        bestvalue = float(bestvalue) / total
        single_word = ( k.find('<w>') >= 0 and k.find('</w>') >= 0)
        if bestvalue >= min_score or (single_word and force_single_word):
          rules[k] = bestkey
  return rules

def PrintTopChoice(count, min_examples, min_score):
  for k,v in count.items():
    # first get total examples
    total = 0
    for c in v.values():
      total += c
    if total >= min_examples:
      bestkey, bestvalue = max(v.iteritems(), key=operator.itemgetter(1))
      if bestkey != GetMiddle(k):
        bestvalue = float(bestvalue) / total
        if bestvalue >= min_score:
          if bestkey == '':
            bestkey = "-"
          ngram = '_'.join( re.split(' ', k))
          print str(bestvalue) + " " + str(total) + " " + ngram + " " + bestkey

def GetMiddle(s):
  pron = re.split(" ", s)
  if len(pron) % 2 == 0:
    return ''
  middle = len(pron) // 2
  return pron[middle]

def GenerateNGramInsertion(pron, left, right, ins):
  context = {}
  k = GenerateKeyString(pron, left, right)
  context[k] = ins
  k = GenerateKeyString(pron, left-1, right+1)
  context[k] = ins
  k = GenerateKeyString(pron, left-2, right+2)
  context[k] = ins
  k = GenerateKeyString(pron, left-3, right+3)
  context[k] = ins
  return context

def GenerateNGramSubstitutions(pron, index, sub):
  context = {}
  k = GenerateKeyString(pron, index, index) # unigram
  context[k] = sub
  k = GenerateKeyString(pron, index-1, index+1) # trigram
  context[k] = sub
  k = GenerateKeyString(pron, index-2, index+2) # 5gram
  context[k] = sub
  k = GenerateKeyString(pron, index-3, index+3) # 7gram
  context[k] = sub
  return context

def GenerateNGramContext(pron, left, right, window):
  context = []
  for i in range(0, window+1):
    context.append( GenerateKeyString(pron, left-i, right+i) )
  return context

def GenerateKeyString(pron, first, last):
  s = ""
  for i in range(first, last+1):
    if i < 0:
      s = s + "<w> "
    elif i >= len(pron):
      s = s + "</w> "
    else:
      s = s + pron[i] + " "
  return s.strip()


def usage():
  print ' --help Prints this message'
  print ' --dictionary= File containing the true dictionary'
  print ' --pronunciation= File containing set of pronunciation hypotheses'
  print ' --examples= Minimum number of examples in order to consider rule'
  print ' --score= Minimum score in order to consider rule'
  print ' --cost= Link to file containing the confusion matrix for phones'
  print ' --force= Add all rules that affect only one word'
  sys.exit(' ')

if __name__ == "__main__":
  main()
