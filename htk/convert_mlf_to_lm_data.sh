#!/bin/bash -xe

# William Hartmann (hartmannw@gmail.com)
# This is free and unencumbered software released into the public domain.
# See the UNLICENSE file for more information.
#
# Script expects a filename pointing to a file that contains a word mlf file
# with no timing information. Assumes all of the files are named with the .lab
# suffix and that the sentence start and end are both sil.

file=$1

sed -e '/MLF/d' -e '/\.lab/d' $file | tr '\n' ' ' | sed -e 's/ \./\n/g' \
    | sed -e 's/^ *sil/<s>/g' | sed -e 's/sil$/<\/s>/g'
