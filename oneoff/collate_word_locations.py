#!/usr/bin/python
#
# William Hartmann (hartmannw@gmail.com)
# This is free and unencumbered software released into the public domain.
# See the UNLICENSE file for more information.
#
# Assuming we have the locations of words spread out in a set of word specific 
# files, this script pulls all of that information into a single file

import getopt, sys, string, re, os.path

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hl:d:m:", 
        ["help", "locationfile=", "directory=", "maxexamples="])
  except getopt.GetoptError:
    usage()

  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
    if o in ("-l", "--locationfile"):
      locationfile = str(a);
    if o in ("-d", "--directory"):
      directory = str(a)
    if o in ("-m", "--maxexamples"):
      maxexamples = int(a)

  words = open(locationfile, 'r')
  for line in words:
    data = re.split(' ', line)
    word = data[0]
    location = directory + "/" + data[1]
    if os.path.exists(location):
      locs = open(location, 'r')
      total = 0
      for line in locs:
        total += 1
        if total > maxexamples:
          break
        print word + " " + line[4:].strip()
      locs.close()
  words.close()

def usage():
  print ' --help Prints this message'
  print ' --locationfile= File containing the names of the word location files'
  print ' --directory= Directory of word location files'
  print ' --maxexamples= Maximum number of examples per word'
  sys.exit(' ')

if __name__ == "__main__":
  main()
