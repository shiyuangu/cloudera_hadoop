#!/usr/bin/python

import sys
import json

for line in sys.stdin:
  user, artists, mixer = line.strip().split("\t")

  # Parse the mixer data as a JSON string.
  mixer_data = json.loads(mixer)
  inter = mixer_data['i']
  # Parse the artists into the artist ids.
  selected_ids = [int(x) for x in json.loads(artists)]

  # Find the index of the lowest-ranked artist that was
  # selected by the user.
  cmax = max([inter.index(x) for x in selected_ids if x in inter])
  cartist = inter[cmax]
 
  # Use the position of cartist in 'a' and 'b' to determine
  # 'k', the smallest value such that the union of a[0:k]
  # and b[0:k] contains all of the artists that were selected.
  a = mixer_data['a']
  b = mixer_data['b']
  if cartist in a:
    k = a.index(cartist)
    if cartist in b:
      k = min(k, b.index(cartist))
  else:
    k = b.index(cartist)
  
  # Determine which of the subranges of a and b contains
  # more of the artists the user selected.
  selected_set = set(selected_ids)
  ha = len(selected_set.intersection(set(a[0:k])))
  hb = len(selected_set.intersection(set(b[0:k])))
  if ha == hb:
    print "tie"
  elif ha > hb:
    print "a"
  else:
    print "b"
