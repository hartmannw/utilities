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
    opts, args = getopt.getopt(sys.argv[1:], "hd:p:", 
        ["help", "dictionary=", "pronunciation="])
  except getopt.GetoptError:
    usage()

  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
    if o in ("-d", "--dictionary"):
      dictfile = str(a);
    if o in ("-p", "--pronunciation"):
      hfile= str(a)

  # Load in the dictionary file
  dictionary = {}
  fin = open(dictfile, "r")
  for line in fin:
    data = re.split(" ", line.strip())
    dictionary[data[0]] = data[1:]
  fin.close()

  count = {}
  fin = open(hfile, "r")
  for line in fin:
    data = re.split(" ", line.strip())
    pron = dictionary[data[0]]
    print line.strip()
    distance, transform = string_manip.EditDistance(pron, data[1:])
    if len(transform) == distance:
      for i in range(len(pron)):
        sub = transform.get(str(i), pron[i])
        context = GenerateNGramSubstitutions(pron, i, sub)
        for k,v in context.items():
          count[k] = count.get(k,{}) # Force it to be set
          count[k][v] = count.get(k,{}).get(v,0) + 1
  fin.close()
  
  # Now to evaluate the results
  PrintTopChoice(count)

def PrintTopChoice(count):
  for k,v in count.items():
    # first get total examples
    total = 0
    for c in v.values():
      total += c
    if total > 0:
      bestkey, bestvalue = max(v.iteritems(), key=operator.itemgetter(1))
      if bestkey != GetMiddle(k):
        bestvalue = float(bestvalue) / total
        print str(bestvalue) + " " + str(total) + " " + k + " " + bestkey

def GetMiddle(s):
  if len(s) % 2 == 0:
    return ''
  middle = len(s) // 2
  return s[middle]

def GenerateNGramSubstitutions(pron, index, sub):
  context = {}
  context[pron[index]] = sub
  return context

def usage():
  print ' --help Prints this message'
  print ' --dictionary= File containing the true dictionary'
  print ' --pronunciation= File containing set of pronunciation hypotheses'
  sys.exit(' ')

if __name__ == "__main__":
  main()
