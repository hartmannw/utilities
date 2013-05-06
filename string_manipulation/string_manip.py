#!/usr/bin/python
#
# William Hartmann (hartmannw@gmail.com)
# This is free and unencumbered software released into the public domain.
# See the UNLICENSE file for more information.
#
# Contains various string manipulation functions.

import operator

# Computes both the edit distance between the two strings, but also the
# necessary steps to transform the target into the guess. Due to the way the
# operations are stored, it only allows one string operation per position. If
# the strings are significantly different in terms of length, then the
# transformations may be incorrect.
def EditDistance(target, guess, cost):
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
        deletion = d[i][j-1]+ cost.get(target[j-1], {}).get("",1)
        insertion = d[i-1][j]+ cost.get("", {}).get(guess[i-1],1)
        substitution = d[i-1][j-1]+ cost.get(target[j-1], {}).get(guess[i-1],1)
        values = [substitution, deletion, insertion]
        minindex, minvalue = min(enumerate(values), key=operator.itemgetter(1))
        d[i][j] = minvalue
        if minindex == 0:
          transform[i][j] = transform[i-1][j-1].copy()
          transform[i][j][str(j-1)] = guess[i-1]
        elif minindex == 1:
          transform[i][j] = transform[i][j-1].copy()
          transform[i][j][str(j-1)] = ""
        else:
          transform[i][j] = transform[i-1][j].copy()
          transform[i][j][str(i-2) + ":" + str(i-1)] = guess[i-1]
  return d[n-1][m-1], transform[n-1][m-1]

