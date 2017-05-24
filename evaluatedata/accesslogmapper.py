#!/usr/bin/python

import datetime
import re
import sys

# For extracting the date and request info from the request.
pattern = re.compile(r"^.*\[(.*)\] \"GET (.*) HTTP/1.1\".*$")

def StandardizeDate(date_str):
  (dt_str, tz) = date_str.split(" ")
  dt = datetime.datetime.strptime(dt_str, "%d/%b/%Y:%H:%M:%S")
  if tz == "-0500":  # East Coast
    dt += datetime.timedelta(hours=5)
  else: # Pacific
    dt += datetime.timedelta(hours=8)
  return dt.strftime("%d/%b/%Y:%H:%M:%S")

def bin_to_int(bin):
  # Converts a binary format number (string) to an integer
  return int(bin, 2)

def FixPlaycounts(request):
  if "/listen?" in request:
    _, request_args = request.split("?")
    artist, playcount_str = request_args.split("&")
    _, playcount = playcount_str.split("=")
    if playcount[0] == '-':
      positive = playcount.lstrip('-')
      return "/listen?%s&playcount=%s" % (artist, bin_to_int(positive))
  return request

for line in sys.stdin:
  line = line.strip()
  res = pattern.match(line)
  if res:
    date_str = res.group(1)
    line = line.replace(date_str, StandardizeDate(date_str))
    request = res.group(2)
    line = line.replace(request, FixPlaycounts(request))
  print line
