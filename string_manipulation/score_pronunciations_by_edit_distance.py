#!/usr/bin/python
#
# William Hartmann (hartmannw@gmail.com)
# This is free and unencumbered software released into the public domain.
# See the UNLICENSE file for more information.
#
# Given a set of true pronunciations and a second file of hypothesized
# pronunciations, each hypothesis is ranked as edit distance / len(true
# pronunciation). The smaller the value, the better.

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

  fin = open(hfile, "r")
  for line in fin:
    data = re.split(" ", line.strip())
    distance, transform = string_manip.EditDistance(dictionary[data[0]], data[1:])
    print str(float(distance) / len(dictionary[data[0]])) + " " + line.strip()
  fin.close()

def usage():
  print ' --help Prints this message'
  print ' --dictionary= File containing the true dictionary'
  print ' --pronunciation= File containing set of pronunciation hypotheses'
  sys.exit(' ')

if __name__ == "__main__":
  main()
