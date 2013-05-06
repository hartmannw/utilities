#!/bin/bash -xe

# William Hartmann (hartmannw@gmail.com)
# This is free and unencumbered software released into the public domain.
# See the UNLICENSE file for more information.
#
# Runs HResults once per file and adds all of the results together.

truemlf=$1
mlf=temp.$$.mlf
cp $truemlf $mlf
hresult_out=temp.pc.$$.txt
pc=temp.pc_strip.$$.txt
result=results.txt
tresult=temp.$$.results

nsents=$( cat $mlf | grep -c '^\.$' )
nsents=10
for (( i=0; $i < $nsents; i=$i+1 ))
do
  echo $i
  HResults -I ~/research/Pronunciation/WSJ0/hmm_training/WSJ0_grapheme_plp_mono/train.phones.mlf -m 1 -p -z nullclass -e nullclass sp \
    -e nullclass '!SENT_END' -e nullclass '!SENT_START' -e nullclass sil \
    ~/research/Pronunciation/WSJ0/htkfiles/grapheme.models.sp \
    $mlf > $hresult_out
  ./parse_phone_confusion.pl $hresult_out  > $pc
  if [ $i -eq 0 ]
  then
    cp $pc $tresult
  else
    ../math/combine_matrix_files.py -a $result $pc > $tresult
  fi
  mv $tresult $result
done

rm $trumlf
