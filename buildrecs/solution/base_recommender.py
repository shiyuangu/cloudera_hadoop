# Import the necessary libraries from MLllib for building a recommender
import re
from pyspark.mllib.recommendation import ALS, Rating

# Import the custom functions that will be used
from functions import *

# Load the fixed access log files from HDFS
data = sc.textFile('/earcloud/accesslogfixed')

# Filter out the non-playcount logs and parse them
playcounts = data.filter(filter_and_match).map(filter_and_match)

# Split the data into training and testing sets
[test, train] = playcounts.randomSplit([0.2, 0.8])

# Cache the RDDs
test.cache()
train.cache()

# Create an ALS recommendation model using the training data
model = ALS.trainImplicit(train, rank=50, lambda_=1.0, alpha=40.0)

# Create a special list of Item IDs to be sent to each piece of the
# parallel calculation
allItemIDs = playcounts.map(lambda x: x.product).distinct().collect()
bAllItemIDs = sc.broadcast(allItemIDs)

# Calculate the AUC for the model
auc = areaUnderCurve(test, bAllItemIDs, model.predictAll)

# Define the different values of hyperparameters for tuning
ranks = [10,50]
lambdas = [1.0, 0.0001]
alphas = [1.0]

# Tune the model using all combinations of the hyperparameters above
(tunevals, bestvals) = tune_hyperparameters(train, test, bAllItemIDs, ranks, lambdas, alphas)

# Print out the AUC for each combination of the hyperparameters
for i in tunevals:
	print i

# Use the hyperaparameter values associated with the highest AUC
# to train the model on the full data set
bestmodel = ALS.trainImplicit(playcounts, rank=bestvals[0], lambda_=bestvals[1], alpha=bestvals[2])

# Create an RDD with user IDs for a subset of the total user population 
# This subgroup will be used to test the different algorithms in production
testusers = sc.parallelize(range(100))

# Use a custom function to generate a list of recommendations
# for the test users using the best model
recommendations = predict_for_testusers(playcounts, bestmodel, testusers)

# Write the recommendations to a local csv file in the format:
#  user_id, ranking, artist_id
write_recs(recommendations, 'base_recommendations.csv')
