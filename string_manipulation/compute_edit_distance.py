#!/usr/bin/python
#
# William Hartmann (hartmannw@gmail.com)
# This is free and unencumbered software released into the public domain.
# See the UNLICENSE file for more information.
#
# Computes the edit distance between two strings and provides the
# transformations necessary to transform the target into the guess.

import getopt, sys, string, re, operator, string_manip

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "ht:g:", 
        ["help", "target=", "guess="])
  except getopt.GetoptError:
    usage()

  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
    if o in ("-t", "--target"):
      target = str(a);
    if o in ("-g", "--guess"):
      guess= str(a)

  print target + " --> " + guess
  target = re.split(' ', target)
  guess = re.split(' ', guess)

  distance, transformations = string_manip.EditDistance(target, guess)
  print distance
  print transformations


def usage():
  print ' --help Prints this message'
  print ' --target= True string'
  print ' --guess= String that is trying to match the target'
  sys.exit(' ')

if __name__ == "__main__":
  main()
