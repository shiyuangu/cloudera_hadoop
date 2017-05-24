# Pre-requisite:
# hadoop fs -getmerge /user/hive/warehouse/word_playcount_counts word_counts.tsv
# R

# Load the R source file containing mutual_info and other
# R functions that have been provided to help us complete
# this exercise.
source("word_functions.R")

# The Bleats data should already be loaded in memory from
# earlier commands you typed during the same R session, but
# if not, uncomment the following line to run the R code to
# create the appropriate vectors from the bleat_counts.csv 
# file containing your Hive query results.
#source("load_bleat_counts.R")

# Load in the word count data
word_counts = read.csv("word_counts.tsv", header=FALSE, sep="\t")
names(word_counts) = c("word", "five_star", "count")

# Aggregate the counts by word.
word_freqs = tapply(word_counts$count, word_counts$word, sum)
word_freqs = sort(word_freqs, decreasing=TRUE)

# How many unique words are there?
length(word_freqs)

# TODO: What's the most frequently occurring word?


# TODO: What about the top 5 most frequent words?


# Let's look at the whole distribution.
plot(word_freqs)  

# TODO: To compute the mutual information, we need to know the number
# of bleated artists that had high play counts:
TOTAL_FIVE_STARS = 

# TODO: We must also know the number of bleated artists that had any play count.
TOTAL_BLEATS = 

# call the function to analyze the word count. This will
# create a list of data frames, one for each word.
scores = analyze_word_counts(word_counts)

# TODO: Sort the scores in descending order
scores = 

# Look at the top five scores.
scores[1:5]

# And the overall distribution.
plot(scores)

# And the distribution of the top 100 scores.
plot(scores[1:100])

# Save the scores and the counts for each word.
save_word_count_data(word_counts, scores)

# Exit R
q()
