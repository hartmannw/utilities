#!/bin/bash -xe

# William Hartmann (hartmannw@gmail.com)
# This is free and unencumbered software released into the public domain.
# See the UNLICENSE file for more information.
#
# Converts the given arpa formatted LM file into a word network file that can 
# be read by HVite for decoding. Assumes the file contains unigrams and bigrams.
# Only the words with a unigram probability appear in the word list.

lm=$1
latfile=$2

tempdir=../temp
tempname=$$
wordlist=$tempdir/convertlm.$tempname.wordlist

# Find the header for 1-grams and 2-grams. A list of all possible words (e.g. 
# unigrams) should exist between these two points.
startline=`grep -nr "1-grams" $lm | cut -d':' -f1`
startline=`expr $startline + 1`
endline=`grep -nr "2-grams" $lm | cut -d':' -f1`
endline=`expr $endline - 2`
sed -n $startline,${endline}p $lm | cut -f2 > $wordlist

cat $wordlist

HBuild -n $lm -s "<s>" "</s>" -z $wordlist $latfile

rm $wordlist
