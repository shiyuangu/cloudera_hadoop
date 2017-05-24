DROP TABLE IF EXISTS USERS;

-- Load the user data.
CREATE EXTERNAL TABLE USERS
(
  id int,
  gender string,
  age int,
  occupation int,
  zipcode string
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LOCATION '/earcloud/userfixed';
