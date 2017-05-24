#!/usr/bin/python

import json
import re
import sys
from nltk import tokenize

# Define the regular expression pattern that we want to match on
ARTIST_PLAYCOUNT_RE = re.compile(".*artist=(\d+)&playcount=(\d+).*")

# Define the threshold over which we'll consider that
# a bleat was a high play count bleat
threshold = 100

def GetArtistAndPlaycount(request):
  m = ARTIST_PLAYCOUNT_RE.match(request)
  if m:
    return (int(m.group(1)), int(m.group(2)))
  else:
    return (None, None)

def GetArtistIdFromBleat(bleat):
  if 'entities' in bleat:
    for link in bleat['entities']['urls']:
      return int((link['url'].split("/"))[-1])
  return None

def ParseBleatText(text):
  # Line below removes the actual artist name form the bleat text
  # (artist name is always contained in single quotes)
  # text = re.sub("'[0-9a-zA-Z]+'", "", text)
  return [w for w in tokenize.wordpunct_tokenize(text.lower()) if len(w) > 2]

for line in sys.stdin:
  (bleats_list, requests) = line.strip().split('\t')

  # First, pull out the user's playcounts
  artist_playcounts = {}
  for request in requests.split(','):
    artist_id, playcount = GetArtistAndPlaycount(request)
    if artist_id:
      artist_playcounts[artist_id] = playcount


  # Then look for artists we have playcounts for in the bleats.
  for item in json.loads(bleats_list):
    bleat = json.loads(item)
    artist_id = GetArtistIdFromBleat(bleat)
    sys.stderr.write("@@@@@@ POINT A %s" % artist_id)
    if artist_id in artist_playcounts:
      high_playcount = 0
      if artist_playcounts[artist_id] >= threshold:
        high_playcount = 1
      for token in set(ParseBleatText(bleat['text'])):
        print "%s\t%d" % (token, high_playcount)
