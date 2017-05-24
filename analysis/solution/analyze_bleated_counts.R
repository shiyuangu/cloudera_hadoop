# Pre-requisite:
# hadoop fs -getmerge /user/hive/warehouse/bleated_playcounts bleat_counts.csv
# R

data = read.csv("bleat_counts.csv", header=FALSE)
names(data) = c("bleated", "high_playcount", "count")
bleated = data[data$bleated == 1, "count"]
not_bleated = data[data$bleated == 0, "count"]

# Give names to the playcounts vectors. The names ("1", "2", etc.)
# become the X-labels when we plot the vectors using R's barplot function.
names(bleated) = sapply(1:5, as.character)
names(not_bleated) = sapply(1:5, as.character)

# Now that we've loaded the data, let's analyze it.

barplot(bleated)   # Distribution of playcounts for bleated artists
barplot(not_bleated)  # Distribution of playcounts for non-bleated artists

# Ratio of bleated to total for each playcount (1-5)
barplot(bleated / (not_bleated + bleated))

# We'll need to use these counts for the next part of the exercise, so hold
# on to them.
