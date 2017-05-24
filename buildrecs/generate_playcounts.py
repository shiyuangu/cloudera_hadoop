#!/usr/bin/python

import csv
import json
import math
import re
import sys
from nltk import tokenize

ARTIST_PLAYCOUNT_RE = re.compile(".*artist=(\d+)&playcount=(\d+).*")

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
  return [w for w in tokenize.wordpunct_tokenize(text.lower()) if len(w) > 2]

def LoadWordScores(file, mi_threshold = 0.001):
  scores = {}
  header = True
  for row in csv.reader(open(file), delimiter="\t"):
    if header:
      # Skip header line.
      header = False
    else:
      word, cnt0, cnt1, mi = row[0], float(row[1]), float(row[2]), float(row[3])
      if mi > mi_threshold:
        cnt0, cnt1 = max(0.5, cnt0), max(0.5, cnt1)
        scores[word] = cnt1 / (cnt0 + cnt1)
  return scores

# Load the word scores we'll need for the Naive Bayes classifier.
PRIOR_PROB = float(29617) / float(40000)
WORD_SCORES = LoadWordScores("word_scores.tsv")

def IsProbablyFiveStar(bleat_text):
  # Log estimates are more stable than multiplying floating point numbers.
  pos_score = math.log(PRIOR_PROB)
  neg_score = math.log(1.0 - PRIOR_PROB)
  for token in set(ParseBleatText(bleat_text)):
    if token in WORD_SCORES:
      pos_score += math.log(WORD_SCORES[token])
      neg_score += math.log(1.0 - WORD_SCORES[token])
  return pos_score > neg_score

for line in sys.stdin:
  (user_id, bleats_list, requests) = line.strip().split('\t')
  user_id = int(user_id)

  # Get the playcounts for artists the user explicitly rated.
  rated_artist_ids = set()

  for request in requests.split(','):
    artist_id, playcount = GetArtistAndPlaycount(request)
    if artist_id:
      rated_artist_ids.add(artist_id)
      print "%d\t%d\t%d" % (user_id, artist_id, playcount)

  # Then look for artists that were bleated, but not rated, and
  # see if we can infer a 5-star playcount from the text.
  for item in json.loads(bleats_list):
    bleat = json.loads(item)
    artist_id = GetArtistIdFromBleat(bleat)
    if artist_id not in rated_artist_ids and IsProbablyFiveStar(bleat['text']):
      print "%d\t%d\t150" % (user_id, artist_id)
