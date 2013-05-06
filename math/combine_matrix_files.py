#!/usr/bin/python
#
# William Hartmann (hartmannw@gmail.com)
# This is free and unencumbered software released into the public domain.
# See the UNLICENSE file for more information.
#
# Combines the matrices stored in each of the files with the specified 
# mathematical operation. Assumes all files contain the same number of rows and
# columns.

import getopt, sys, string, re

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hasmdf", 
        ["help", "add", "subtract", "multiply", "divide", "float"])
  except getopt.GetoptError:
    usage()

  use_float = False
  perform_add = False
  perform_subtract = False
  perform_multiply = False
  perform_divide = False
  total_operations = 0;

  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
    if o in ("-a", "--add"):
      perform_add = True
      total_operations += 1
    if o in ("-s", "--subtract"):
      perform_subtract = True
      total_operations += 1
    if o in ("-m", "--multiply"):
      perform_multiply = True
      total_operations += 1
    if o in ("-d", "--divide"):
      perform_divide = True
      total_operations += 1
    if o in ("-f", "--float"):
      use_float = True

  if total_operations != 1:
    print ' You must specify exacly one operation (-a -s d -m)'
    usage()
  if len(args) < 2:
    print ' You must provide at least two text files'
    usage()

  result = LoadMatrix(args[0], use_float)
  for file_name in args[1:]:
    data = LoadMatrix(file_name, use_float)
    if perform_add:
      result = [map( lambda x,y:x+y, result[i], data[i]) for i in range(len(result)) ]
    elif perform_subtract:
      result = [map( lambda x,y:x-y, result[i], data[i]) for i in range(len(result)) ]
    elif perform_divide:
      result = [map( lambda x,y:x/y, result[i], data[i]) for i in range(len(result)) ]
    elif perform_multiply:
      result = [map( lambda x,y:x*y, result[i], data[i]) for i in range(len(result)) ]

  for r in result:
    print " ".join(map(str, r))

def LoadMatrix(file_name, use_float):
  fin = open(file_name, 'r')
  if use_float == True:
    ret = [ map(float,line.split(' ')) for line in fin ]
  else:
    ret = [ map(int,line.split(' ')) for line in fin ]
  fin.close()

  return ret

def usage():
  print ' --help Prints this message'
  print ' --add Adds the files'
  print ' --subtract Subtracts all files from the first'
  print ' --multiply Elementwise multiplication.'
  print ' --divides Divides the first file by all other files'
  print ' --float Treat all values as float (default is int)'
  sys.exit(' ')

if __name__ == "__main__":
  main()
