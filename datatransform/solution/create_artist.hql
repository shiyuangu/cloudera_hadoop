DROP TABLE IF EXISTS ARTIST;

-- Load the artist data.
CREATE EXTERNAL TABLE ARTIST
(
  id int,
  name string,
  year int
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LOCATION '/earcloud/artistfixed';
