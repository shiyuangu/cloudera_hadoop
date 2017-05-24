import re
import random
import itertools
from pyspark.mllib.recommendation import ALS, Rating

def filter_and_match(line):
  # This function returns False if the line doesn't match the Regular expression
  # and returns the user, artist and playcount if the line matches the pattern
  expr = ".*GET /listen\?artist=(\\d+)&playcount=(\\d+) HTTP/1.1.*USER=(\\d+)"
  match = re.match(expr,line)
  if match:
    return Rating(int(match.group(3)), int(match.group(1)), int(match.group(2)))
  else:
    return False

def parse_line(line):
  # This function parses a simple csv input of user, artist, rating
  line = line.split(',')
  return Rating(int(line[0]), int(line[1]), int(float(line[2])))

def positiveNegativeCompareMapper((positiveRatings, negativeRatings)):
  # This function compares all pairs of elements between two lists
  # and returns the percentage of items in the first list 
  # that were ranked higher
  correct = 0
  total = 0
  for pos in positiveRatings:
    for neg in negativeRatings:
      if pos.rating > neg.rating:
        correct += 1
      total += 1
  return float(correct)/total

def positiveUserProductsMapper(partno, userIDAndPosItemIDs, bAllItemIDs):
  # This function generates a list of ratings for items that a user has not rated 
  # that is the same length as the list of items that they have rated
  # from the test data set
  allItemIDs = bAllItemIDs.value
  random.seed(partno)
  for input in userIDAndPosItemIDs:
    (userID, posItemIDs) = input
    posItemIDSet = set(posItemIDs)
    negative = []
    i = 0
    while i < len(allItemIDs) and (len(negative) < len(posItemIDSet)):
      itemID = random.choice(allItemIDs)
      if itemID not in posItemIDSet:
        negative.append((userID, itemID))
      i += 1
    yield negative


def areaUnderCurve(positiveData, bAllItemIDs, predictFunction):
  # What this actually computes is AUC, per user. 
  # The result is actually something that might be called "mean AUC".
  # Take held-out data as the "positive", and map to tuples
  positiveUserProducts = positiveData.map(lambda x: (x.user, x.product))
  # Make predictions for each of them, including a numeric score, and gather by user
  positivePredictions = predictFunction(positiveUserProducts).groupBy(lambda x: x.user)
  # BinaryClassificationMetrics.areaUnderROC is not used here since there 
  # are really lots of small AUC problems, and it would be inefficient, when
  # a direct computation is available.
  # Create a set of "negative" products for each user. These are randomly 
  # chosen from among all of the other items, excluding those that are 
  # "positive" for the user.
  negativeUserProducts = positiveUserProducts.groupByKey().mapPartitionsWithIndex(lambda x, y: positiveUserProductsMapper(x, y, bAllItemIDs)).flatMap(lambda x: x)
  # flatMap breaks the collections above down into one big set of tuples   
  # Make predictions on the rest:
  negativePredictions = predictFunction(negativeUserProducts).groupBy(lambda x: x.user)
  return positivePredictions.join(negativePredictions).values().map(positiveNegativeCompareMapper).mean()


def tune_hyperparameters(train, test, bAllItemIDs, ranks, lambdas, alphas):
  # This function takes lists of hyperparameters, trains a model using 
  # all combinations of the parameters in these lists, calculates AUC
  # for each of the models, then returns a list with AUC and hyperparamter 
  # combinations. It also returns a second value that is a list containing only
  # the hyperparameters that correspond to the highest AUC
  tuned_vals = []
  best_auc = 0
  for rank, alpha, lambda_ in itertools.product(ranks, alphas, lambdas):
    print "Training mode for (rank, lambda, alpha) = ({rank},{lambda_},{alpha})".format(rank=rank, lambda_=lambda_, alpha=alpha)
    model = ALS.trainImplicit(train, rank=rank, lambda_=lambda_, alpha=alpha)
    auc = areaUnderCurve(test, bAllItemIDs, model.predictAll)
    tuned_vals.append([auc, rank, lambda_, alpha])
    if auc > best_auc:
      best_model = [rank, lambda_, alpha]
      best_auc = auc
  return (tuned_vals, best_model)
		
def predict_for_testusers(playcounts, model, testusers):
  # This function take an RDD of a subset of testusers to make predicitons for
  # and uses the model to predict the top 10 recommendations for each user.
  # This function is written in such a way as to not max out the JVM heap space.
  testusergroups = testusers.randomSplit([0.5 for i in range(2)])

  artists = playcounts.map(lambda x: x.product).distinct()

  allrecs = []

  for tug in testusergroups:
    userartist = tug.cartesian(artists)
    recs = model.predictAll(userartist)
    out = recs.map(lambda x: [x.user, x.rating, x.product]).groupBy(lambda x: x[0]).map(lambda x: sorted(list(x[1]), key=lambda x: -x[1])[:10]).flatMap(lambda x: x).collect()
    allrecs.extend(out)

  return allrecs

def write_recs(recs, filename):
  # This function writes a list of recommendations out to a 
  # comma separated file on the local filesystem
  recs.sort(key=lambda x: x[0])
  f = open(filename, 'w')
  for rec in recs:
    line = ",".join([str(i) for i in rec]) + '\n'
    f.write(line)

  f.close()
