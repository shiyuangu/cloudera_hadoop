#!/usr/bin/env python

# The line above tells the UNIX shell that we want
# the Python interpreter to execute this script.

# The next two lines import the 're' (regular 
# expression) and 'sys' (system) modules.  The
# 're' module allows us to match complex patterns
# in strings, while the 'sys' module allows us
# to read from the standard input stream as well
# as write to the standard error stream.
import re
import sys

# The regular expression pattern we'll use to parse
# individual fields from the Apache log file.  Here's
# the order in which those fields appear, along with 
# a brief description and an example.  Note that the 
# user agent (browser) field is very long and the 
# example value shown here has been truncated so that
# it will fit into the table.
#
# Index Field        Example value
# ----- ------------ ----------------------------------------------------
#    1 	IP address   192.168.13.2
#    2	Ident        -  (seldom populated on modern servers)
#    3	User         -  (never used in this log)
#    4	Date/Time    [22/Sep/1997:15:01:46 -0800]
#    5	Request      "GET /listen?artist=1000239&playcount=209 HTTP/1.1"
#    6	Status code  200
#    7	Bytes sent   7
#    8	Referer      "http://earcloud.com/"
#    9	User agent   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) ..."
#   10	Cookie       "USER=29"
#
# NOTE: the pattern itself contains double quotes, so we use single quotes
# to define the string so we don't have to escape embedded double quotes.
pattern = '(\d+\.\d+\.\d+\.\d+) (.*) (.*) \[(.*)\] "(.*)" (\d+) (.*) "(.*)" "(.*)" "(.*)"'

# We must compile this string into a regular 
# expression object before we can use it.
regex = re.compile(pattern)

# We're going to count the operating systems used to 
# access our site, based on the contents of the user 
# agent field.  We need to initialize the variables
# we'll use to keep track of each type.
iphone = 0
mac = 0
windows = 0
android = 0

# read each line from the standard input stream
for line in sys.stdin:

  # strip off the leading and trailing whitespace
  # characters from the string for consistency
  line = line.strip()

  # try to match the line with our regular expression
  match = regex.match(line)

  # if we did match, extract the 9th (user agent) field
  if match:
    field = match.group(9)

    # check for substrings indicating the operating system
    # NOTE: the iPhone user agent also contains the string 
    # 'Mac OS X', so we must check for iPhone before we 
    # check for Mac OS X.
    if "iPhone" in field:
      iphone = iphone + 1
    elif "Mac OS X" in field:
      mac = mac + 1
    elif "Android" in field:
      android = android + 1
    elif "Windows" in field:
      windows = windows + 1
    else:
      sys.stderr.write("ERROR: Unknown user agent '%s'\n" % field)

  # if we didn't match, print a warning to standard error
  else:
    sys.stderr.write("ERROR: Could not parse line '%s'" % line)

# add up all values to get the total number of requests
total = iphone + mac + android + windows

# print out the total number of requests
print "There were %i total requests" % total

# print out the number of requests by type
print "  iPhone requests:  %i" % iphone
print "  Mac requests:     %i" % mac
print "  Android requests: %i" % android
print "  Windows requests: %i" % windows
