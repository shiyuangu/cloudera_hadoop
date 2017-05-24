# Load the artist data from HDFS
artist = sc.textFile('/earcloud/artist/')

# Look at the first 10 records
artist.take(10)

# Use a map to extract the year from each line,
# then find the distinct values for each year
mapped = artist.map(lambda x: x.split('\t')[2])
distinct_years = mapped.distinct().collect()

# Import the function 'fix_year' that we can 
# use with a mapper to fix the year values
from artist_functions import fix_year
artist_fix = artist.map(fix_year)

# Now check that the years have been fixed
artist_fix.map(lambda x: x.split('\t')[2]).distinct().collect()

# Save the fixed data to HDFS
artist_fix.saveAsTextFile('/earcloud/sparkartist')
