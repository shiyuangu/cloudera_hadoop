#!/usr/bin/env python
import json
import urllib2

# Base URL of the Bleater REST API site
site = "http://bleats.example.com:8080/bleats"

# (A) replace CSVPATH with the path of your CSV file
csv = open("/home/training/training_materials/data_science/data/bleater_ids.csv", "rb")

# This is the file your program will populate with the
# bleats of all users in the CSV file referenced above
output = open("bleatsdownload.json","wb")

print "Starting bleat downloads..."

for line in csv:
  try:
    # (B) strip and split the string on commas, then store
    # the Bleater user ID in the bleater_id variable
    fields = line.strip().split(",")
    bleater_id = fields[1]
    print "\tDownloading bleats for Bleater ID %s" % bleater_id
  except:
    print "Skipping line '%s'" % line.strip()
    continue

  # (C) Assign the url variable with a value that represents
  # the REST API address for the current user ID's bleats,
  # as described in the exercise manual.
  url = "%s/%s" % (site, str(bleater_id))

  # (D) Now read the JSON from this URL (using the urllib2 and json
  # libraries imported above) and write each bleat received to the output
  # file, followed by a newline character.  Every bleat must be written
  # out on a line by itself.
  bleats = json.loads(urllib2.urlopen(url).read())
  for bleat in bleats:
    output.write(json.dumps(bleat) + "\n")

output.close()

print "Downloads complete"
