#!/usr/bin/env python

import sys

for line in sys.stdin:
  try:
    # Format of input: ID\tName\tYear
    # Here we strip the line of leading and trailing whitespace,
    # then split into the three fields based on a tab delimiter
    (id, name, year) = line.strip().split("\t")

    # this tells Hadoop to count the records we parsed sucessfully
    sys.stderr.write("reporter:counter:ARTIST,PROCESSED_LINES,1\n")
  except:
    # this tells Hadoop to count the records we failed to parse
    sys.stderr.write("reporter:counter:ARTIST,SKIPPED_LINES,1\n")
    continue

  # Here we cast the year to an integer so we can check 
  # its value numerically
  year = int(year)

  # TODO (A): Handle the case of negative year (-1989)

  # TODO (B): Handle the case of two digit year (89)

  # print the corrected line to standard output
  print "%s\t%s\t%s" % (id, name, str(year))
