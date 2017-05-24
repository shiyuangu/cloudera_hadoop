#!/usr/bin/python

import json
import re
import sys
import random

ARTIST_PLAYCOUNT_RE = re.compile(".*artist=(\d+)&playcount=(\d+).*")

def BucketPlaycount(playcount):
  # This function is used to bucket the values of playcounts
  playcount = int(playcount)
  if playcount <= 100:
    return 0
  elif playcount <= 200:
    return 1
  elif playcount <= 300:
    return 2
  elif playcount <= 400:
    return 3
  else:
    return 4

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


for line in sys.stdin:
  (bleats_list, requests) = line.strip().split('\t')

  bleated_artists = set()
  for item in json.loads(bleats_list):
    bleat = json.loads(item)
    artist_id = GetArtistIdFromBleat(bleat)
    if artist_id:
      bleated_artists.add(artist_id)

  for request in requests.split(','):
    artist_id, playcount = GetArtistAndPlaycount(request)
    if artist_id:
      if artist_id in bleated_artists:
        print "1\t%d" % BucketPlaycount(playcount)
      else:
        print "0\t%d" % BucketPlaycount(playcount)
