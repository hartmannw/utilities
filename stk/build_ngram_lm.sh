#!/bin/bash -xe

# William Hartmann (hartmannw@gmail.com)
# This is free and unencumbered software released into the public domain.
# See the UNLICENSE file for more information.
#
# Expects a set of properly formatted data and a LM name. A wordlist is created
# from the data and a count file is generated. The count file is then 
# transformed into an ARPA formatted LM.

data=$1
lm=$2
ngram=$3
ncounts=`expr $ngram + 1`
tempdir=../temp
tempname=$$
counts=$tempdir/buildlm.${tempname}.counts
wordlist=$tempdir/buildlm.${tempname}.wordlist

cat $data | tr ' ' '\n' | sed -e '/^$/d' | sort -u > $wordlist

engram -c -u -t0 -n${ncounts} -o $counts -l $wordlist $data
engram -u -n${ngram} -t0 $counts -o $lm

# Removing the tabs because they seeme to bother other programs like moses and
# HTK.
cat $lm | sed -e 's/ /\t/g' | sed -e 's/ngram\t/ngram /g' > $lm.tab
mv $lm.tab $lm

# Clean up temporary files.
rm $counts
rm $wordlist
