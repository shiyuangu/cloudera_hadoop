#!/usr/bin/env python
import json
import urllib2

# Base URL of the Bleater REST API site
site = "http://bleats.example.com:8080/bleats"

# TODO (A) replace CSVPATH with the path of your CSV file
csv = open("CSVPATH", "rb")

# This is the file your program will populate with the
# bleats of all users in the CSV file referenced above
output = open("bleatsdownload.json","wb")

print "Starting bleat downloads..."

for line in csv:
  try:
    # strip and split the string on commas, then store
    # the Bleater user ID in the bleater_id variable
    bleater_id = # TODO (B)
    print "\tDownloading bleats for Bleater ID %s" % bleater_id
  except:
    print "Skipping line '%s'" % line.strip()
    continue

  # Assign the url variable with a value that represents
  # the REST API address for the current user ID's bleats,
  # as described in the exercise manual.
  url = # TODO (C)

  # TODO (D): Now read the JSON from this URL (using the urllib2 and json
  # libraries imported above) and write each bleat received to the output
  # file, followed by a newline character.  Every bleat must be written
  # out on a line by itself.


output.close()

print "Downloads complete"
