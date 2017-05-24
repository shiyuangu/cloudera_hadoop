# These are R functions provided for you to calculate
# some statistical properties needed in this lab.

# Load the entropy package, which is pre-installed on the VM.
library(entropy)

# This function for calculating mutual information. The arguments 
# are both (possibly empty) single-valued vectors that contain the 
# number of high play count and non high play count bleats that featured a 
# particular word.
mutual_info = function(high_playcounts, non_high_playcounts) {
  # The high_playcounts and non_high_playcounts values may be empty vectors,
  # so we use the value of 0 for their counts as a default.
  x1 = ifelse(length(high_playcounts) == 0, 0, high_playcounts)
  x2 = ifelse(length(non_high_playcounts) == 0, 0, non_high_playcounts)

  # Use the totals we calculated above to complete the counts we
  # need for the mutual information count matrix.
  x3 = TOTAL_HIGH_PLAYCOUNT - x1
  x4 = TOTAL_BLEATS - TOTAL_HIGH_PLAYCOUNT - x2

  # Construct a matrix from the counts
  count_matrix = rbind(c(x1, x2), c(x3, x4))  

  # Compute the mutual information from the matrix of counts. R functions
  # automatically return the value of the last statement. The 'mi.plugin'
  # function is provided by the 'entropy' package that we loaded above.
  mi.plugin(count_matrix, unit="log2")
}

# This function computes the mutual information for a word based
# on a data frame with two rows and two columns ('count' and
# 'high_playcount'):
#
# count high_playcount
# 12    0
# 17    1
#
# For this example, the word appeared in 17 bleats that received
# five stars and in 12 bleats that did not receive five stars.
mutual_info_for_word = function(word_data) {
  # Get the number of five-star bleats for this word.
  high_playcounts = with(word_data, count[high_playcount == 1])

  # Get the number of non-five-star bleats for this word.
  not_high_playcounts = with(word_data, count[high_playcount == 0])

  # Compute the mutual information for this word.
  mutual_info(high_playcounts, not_high_playcounts)
}

# Computes the mutual information for every word in the word count
# matrix, which should have three columns ('word', 'high_playcount', and
# 'count') and the following structure:
#
# word  count   high_playcount
# foo   17      0
# foo   29      1
# bar   100     0
# bar   2       1
# ...
#
# The function will return a sorted vector of mutual information
# scores for each word.
analyze_word_counts = function(word_counts) {
  # Split the data frame that contains all of the words and their
  # counts into a list of data frames, one data frame for each word.
  word_data_frames = split(word_counts, word_counts$word)

  # Iterate over the list of data frames and compute the mutual information
  # for each word, using the 'mutual_info_for_word' function we defined above.
  sapply(word_data_frames, mutual_info_for_word)
}

# Function to save the scores and the counts for each word
# to a tab-delimited file named word_scores.tsv
save_word_count_data = function(word_counts, scores) {
  # Convert the vector of scores into a data frame.
  scores_data = data.frame(word=names(scores), mi=scores)

  # Use the reshape function to pivot the word count data so that both the high play count and
  # non high play counts are in the same row of the table.
  pivot = reshape(word_counts, v.names="count", idvar="word", timevar="high_playcount", direction="wide")

  # Join the pivot table with the scores data on the common 'word' column.
  out_data = merge(pivot, scores_data)

  # Save the out_data to a TSV file named 'word_scores.tsv' in the current directory.
  write.table(out_data, "word_scores.tsv", sep="\t", na="0", quote=FALSE, row.names=FALSE)
}
