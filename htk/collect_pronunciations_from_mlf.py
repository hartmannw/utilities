#!/usr/bin/python
#
# William Hartmann (hartmannw@gmail.com)
# This is free and unencumbered software released into the public domain.
# See the UNLICENSE file for more information.
#
# Takes two files. One is a word MLF with timing information. The other is a
# list containing the following information (word, file-id, start, end).

import getopt, sys, string, re

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hm:l:", ["help", "mlf=", "list="])
  except getopt.GetoptError:
    usage()

  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
    if o in ("-m", "--mlf"):
      mlf = str(a);
    if o in ("-l", "--list"):
      locationlist = str(a)

  sentid = LoadSentenceLocations(mlf)
  FindPronunciations(mlf, locationlist, sentid)

def FindPronunciations(mlf, locationlist, sentid):
  mlffile = open(mlf, 'r')
  locationfile = open(locationlist, 'r')
  minoverlap = 0.1

  for line in locationfile:
    data = re.split(' ', line)
    word = { 'name': data[0].strip(), 
        'sent': data[1].strip(), 
        'start': int(data[2]), 
        'end': int(data[3])}
    mlffile.seek(sentid[ word['sent'] ])
    line = mlffile.readline()
    foundstart = False
    pron = []
    while foundstart == False:
      line = mlffile.readline()
      data = re.split(' ', line)
      phone = { 'name': data[2].strip(),
          'start': int(data[0]) / 100000,
          'end': int(data[1]) / 100000}
      if phone['end'] > word['start']:
        foundstart = True
        phonelength = phone['end'] - phone['start']
        overlap = (phone['end'] - word['start']) / phonelength
        # If at least half of the phone exists in the word span, we will 
        # consider it part of the pronunciation.
        if overlap >= minoverlap:
          pron.append(phone['name'])
    foundend = False
    while foundend == False:
      line = mlffile.readline()
      data = re.split(' ', line)
      if len(data) < 3:
        break
      phone = { 'name': data[2].strip(),
          'start': int(data[0]) / 100000,
          'end': int(data[1]) / 100000}
      if phone['end'] >= word['end']:
        foundend = True
        phonelength = phone['end'] - phone['start']
        overlap = (word['end'] - phone['start']) / phonelength
        # If at least half of the phone exists in the word span, we will 
        # consider it part of the pronunciation.
        if overlap >= minoverlap:
          pron.append(phone['name'])
      else:
        pron.append(phone['name'])

    if len(pron) > 0:
      PrintPronunciation(word['name'], pron)

  mlffile.close()
  locationfile.close()

# Loads the location of each of the sentences so that we can later seek.
def LoadSentenceLocations(mlf):
  sentid = dict()
  f = open(mlf, 'r')
  offset = 0;
  for line in f:
    if string.find(line, ".rec") >= 0:
      sentid[ line[3:11] ] = offset
    offset += len(line)
  f.close()
  return sentid

def PrintPronunciation(word, pron):
  print word + " " + " ".join(pron)

def usage():
  print ' --help Prints this message'
  print ' --mlf= Location of the MLF file'
  print ' --list= Location of the file containing word locations'
  sys.exit(' ')

if __name__ == "__main__":
  main()
