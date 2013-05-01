#!/usr/bin/python
#
# William Hartmann (hartmannw@gmail.com)
# This is free and unencumbered software released into the public domain.
# See the UNLICENSE file for more information.
#
# Computes the edit distance between two strings and provides the
# transformations necessary to transform the target into the guess.

import getopt, sys, string, re, operator

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

  distance, transformations = EditDistance(target, guess)
  print distance
  print transformations

def EditDistance(target, guess):
## Rewrite going from 0 to len(target), I need the extra row and column
## to keep track of transformations
  n = len(guess) + 1
  m = len(target) + 1
  d = [[ 0 for i in range(m)] for j in range(n)]
  transform = [[ {} for i in range(m)] for j in range(n)]

  for i in range(1,n):
    d[i][0]=i
    transform[i][0] = transform[i-1][0].copy()
    transform[i][0][str(i-2) + ":" + str(i-1)] = guess[i-1]
  
  for j in range(1,m):
    d[0][j]=j
    transform[0][j] = transform[0][j-1].copy()
    transform[0][j][str(j-1)] = ""
  
  for i in range(1,n):
    for j in range(1,m):
      if guess[i-1] == target[j-1]:
        d[i][j] = d[i-1][j-1]
        transform[i][j] = transform[i-1][j-1].copy()
      else:
        deletion = d[i][j-1]+ 1
        insertion = d[i-1][j]+ 1
        substitution = d[i-1][j-1]+ 1
        values = [substitution, deletion, insertion]
        minindex, minvalue = min(enumerate(values), key=operator.itemgetter(1))
        d[i][j] = minvalue
        if minindex == 0:
          transform[i][j] = transform[i-1][j-1].copy()
          transform[i][j][str(i-1)] = guess[j-1]
        elif minindex == 1:
          transform[i][j] = transform[i][j-1].copy()
          transform[i][j][str(j-1)] = ""
        else:
          transform[i][j] = transform[i-1][j].copy()
          transform[i][j][str(i-2) + ":" + str(i-1)] = guess[i-1]

  print d
  print transform
  return d[n-1][m-1], transform[n-1][m-1]

def usage():
  print ' --help Prints this message'
  print ' --target= True string'
  print ' --guess= String that is trying to match the target'
  sys.exit(' ')

if __name__ == "__main__":
  main()
