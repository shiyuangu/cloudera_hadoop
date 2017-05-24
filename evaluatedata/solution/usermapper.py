#!/usr/bin/env python

import sys

for line in sys.stdin:
  try:
    # Format of input: Format: ID\tGender\tAge\tOccupationID\tZip
    # Here we strip the line of leading and trailing whitespace,
    # then split into the five fields based on a tab delimiter
    (id, gender, age, occupation, zip) = line.strip().split("\t")

    # this tells Hadoop to count the records we parsed sucessfully
    sys.stderr.write("reporter:counter:USERS,PROCESSED_LINES,1\n")
  except:
    # this tells Hadoop to count the records we failed to parse
    sys.stderr.write("reporter:counter:USERS,SKIPPED_LINES,1\n")
    continue

  # TODO (A): Normalize all genders (m, M, f or F) to uppercase (M or F)
  gender = gender.upper()

  # TODO (B): Convert any ZIP+4 codes (12345-6789) to the
  #       five-digit representation (12345).
  if len(zip) > 5:
     zip = zip[:5] # First 5 characters

  # Here we cast the age to an integer so we can check 
  # its value numerically
  age = int(age)

  # TODO (C): Convert all ages to absolute (positive) values 
  age = abs(age)

  # print the corrected line to standard output
  print "%s\t%s\t%s\t%s\t%s" % (id, gender, str(age), occupation, zip)
