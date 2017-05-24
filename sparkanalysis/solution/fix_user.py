# Load the user data from HDFS
user = sc.textFile('/earcloud/user/')

# Count the number of records that have an incorrect format
user.filter(lambda x: len(x.split('\t')[4]) > 5).count()

# Count the total number of user records
user.count()

# Import the function that we'll use in a 
# map to fix the user data
from user_functions import fix_user
user_fix = user.map(fix_user)

# Save the corrected user data to HDFS
user_fix.saveAsTextFile('/earcloud/sparkuser')
