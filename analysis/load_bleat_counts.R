# Pre-requisite:
# hadoop fs -getmerge /user/hive/warehouse/bleated_playcounts bleat_counts.csv
# R

data = read.csv("bleat_counts.csv", header=FALSE)
names(data) = c("bleated", "playcount", "count")
bleated = data[data$bleated == 1, "count"]
not_bleated = data[data$bleated == 0, "count"]

# Give names to the playcounts vectors. The names ("1", "2", etc.)
# become the X-labels when we plot the vectors using R's barplot function.
names(bleated) = sapply(1:5, as.character)
names(not_bleated) = sapply(1:5, as.character)

# Now that we've loaded the data, let's analyze it. Follow the exercise
# instructions for the commands to use to visualize the data in R, or 
# look at the 'sample_solution/analyze_bleated_counts.R' file for a hint.
