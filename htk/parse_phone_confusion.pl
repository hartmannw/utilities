#!/usr/bin/perl
#
# William Hartmann (hartmannw@gmail.com)
# This is free and unencumbered software released into the public domain.
# See the UNLICENSE file for more information.
#
# Given the output from HResults, the phone confusion matrix is edited out such 
# that only the values remain separated by a single space. Assumes a properly 
# formatted file without regularities.

$file = $ARGV[0];

open(FIN, $file);
$line = <FIN>;
chomp($line);
while($line !~ m/Confusion Matrix/)
{
  $line = <FIN>;
  chomp($line);
}
$line = <FIN>;
chomp($line);
@phones = split(" ", $line); # Gives us number of phones
$phone_count = @phones;

$line = <FIN>; $line = <FIN>; # Skip two uneeded lines.

# Process one line for each phone.
for($i = 0; $i < ($phone_count); $i++)
{
  $line = <FIN>; chomp($line);
  @data = split(" ", $line);
  $phones[$i] = $data[0]; # Store the true phones
  for($j = 1; $j < ($phone_count +1); $j++)
  {
    print $data[$j] . " ";
  }
  print $data[$phone_count + 1] . "\n";
}

# Process the final line for the Ins.
$line = <FIN>; chomp($line);
@data = split(" ", $line);
for($j = 1; $j < ($phone_count); $j++)
{
  print $data[$j] . " ";
}
print $data[$phone_count] . "\n";

