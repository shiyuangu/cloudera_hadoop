# In order to run this as a script using spark-submit,
# the spark context has to be defined
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName('BleatsRecs').setMaster('local[*]')
sc = SparkContext(conf=conf)

# Import the necessary libraries from MLllib for building a recommender
from pyspark.mllib.recommendation import ALS, Rating

# Import the custom functions that will be used
from functions import *

# Load the fixed access log files from HDFS
data = sc.textFile('/user/hive/warehouse/bleats_input')

# Filter out the non-playcount logs and parse them
playcounts = data.map(parse_line)

# Split the data into training and testing sets
[test, train] = playcounts.randomSplit([0.2, 0.8])

# Create a special list of Item IDs to be sent to 
# each piece of the parallel calculation
allItemIDs = playcounts.map(lambda x: x.product).distinct().collect()
bAllItemIDs = sc.broadcast(allItemIDs)

# Define the different values of hyperparameters for tuning
ranks = [50]
lambdas = [0.0001]
alphas = [1.0]

print "Determining AUC for optimal parameters from base recommender..."
# Tune the model using all combinations of the hyperparameters above
(tunevals, bestvals) = tune_hyperparameters(train, test, bAllItemIDs, ranks, lambdas, alphas)

print "-"*10
print "AUC={auc}".format(auc=tunevals[0][0])
print "-"*10

# Use the hyperaparameter values associated with the highest AUC
# to train the model on the full data set
bestmodel = ALS.trainImplicit(playcounts, rank=bestvals[0], lambda_=bestvals[1], alpha=bestvals[2])

# Create an RDD with user IDs for a subset of 5% of the total user population
# This subgroup will be used to test the different algorithms in production
testusers = sc.parallelize(range(100))

# Use a custom function to generate a list of recommendations
# for the test users using the best model
recommendations = predict_for_testusers(playcounts, bestmodel, testusers)

# Write the recommendations to a local csv file in the format:
#  user_id, ranking, artist_id
write_recs(recommendations, 'bleat_recommendations.csv')
