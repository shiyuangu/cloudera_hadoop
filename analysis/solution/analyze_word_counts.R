# Pre-requisite:
# hadoop fs -getmerge /user/hive/warehouse/word_playcount_counts word_counts.tsv
# R

# Load the R source file containing mutual_info and other
# R functions that have been provided to help us complete
# this exercise.
source("word_functions.R")

# Load in the data.
word_counts = read.csv("word_counts.tsv", header=FALSE, sep="\t")
names(word_counts) = c("word", "high_playcount", "count")

# Aggregate the counts by word.
word_freqs = tapply(word_counts$count, word_counts$word, sum)
word_freqs = sort(word_freqs, decreasing=TRUE)

# How many unique words are there?
length(word_freqs)

# TODO: What's the most frequently occurring word?
word_freqs[1]

# TODO: What about the top 5?
word_freqs[1:5]

# Let's look at the whole distribution.
plot(word_freqs)  # Observe the power law (Zipf) distribution.

# To compute the mutual information, we need to know the number of
# bleated artists that received 5 stars:
TOTAL_HIGH_PLAYCOUNT = sum(bleated[2:5])

# We must also know the number of bleated artists that had any playcount.
TOTAL_BLEATS = sum(bleated)

scores = analyze_word_counts(word_counts)

# TODO: Sort the scores in descending order
scores = sort(scores, decreasing=TRUE)

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
