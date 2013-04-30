#!/usr/bin/python
#
# William Hartmann (hartmannw@gmail.com)
# This is free and unencumbered software released into the public domain.
# See the UNLICENSE file for more information.
#
# Computes the edit distance between two strings.

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

  print guess + " --> " + target
  target = re.split(' ', target)
  guess = re.split(' ', guess)

  distance, transformations = EditDistance(target, guess)
  print distance
  print transformations

def EditDistance(target, guess):
## Rewrite going from 0 to len(target), I need the extra row and column
## to keep track of transformations
  d = [[ 0 for i in range(len(target))] for j in range(len(guess))]
  transform = [[ {} for i in range(len(target))] for j in range(len(guess))]
  for i in range(len(guess)):
    for j in range(len(target)):
      if guess[i] == target[j]:
        d[i][j] = GetValue(d, i-1, j-1)
        transform[i][j] = GetTransform(transform, i-1, j-1).copy()
      else:
        deletion = GetValue(d, i, j-1) + 1
        insertion = GetValue(d, i-1, j) + 1
        substitution = GetValue(d, i-1, j-1) + 1
        values = [substitution, deletion, insertion]
        minindex, minvalue = min(enumerate(values), key=operator.itemgetter(1))
        d[i][j] = minvalue
        if minindex == 0:
          transform[i][j] = GetTransform(transform, i-1, j-1).copy()
          transform[i][j][str(i)] = target[j]
        elif minindex == 1:
          transform[i][j] = GetTransform(transform, i, j-1).copy()
          transform[i][j][str(i)] = ""
        else:
          transform[i][j] = GetTransform(transform, i-1, j).copy()
          transform[i][j][str(i) + ":" + str(i+1)] = target[j]

  print d
  print transform
  return d[len(guess)-1][len(target)-1], transform[len(guess)-1][len(target)-1]


def GetValue(d, i, j):
  if min(i,j) < -1:
    return int("inf")
  if min(i,j) < 0:
    return max(i,j) + 1
  return d[i][j]

def GetTransform(t, i, j):
  if i < 0:
    return GetTransform(t, 0, j)
  if j < 0:
    return GetTransform(t,i,0)
  return t[i][j]

def usage():
  print ' --help Prints this message'
  print ' --target= True string'
  print ' --guess= String that is trying to match the target'
  sys.exit(' ')

if __name__ == "__main__":
  main()
