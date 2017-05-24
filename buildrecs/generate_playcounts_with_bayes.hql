DROP TABLE IF EXISTS BLEATS_INPUT;

-- Create a table we can use to store the playcounts for the
-- improved recommendations
CREATE TABLE BLEATS_INPUT (user int, artist int, playcount double)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

-- The next Hive query that will use the Naive Bayes model to 
-- create playcounts for artists that users liked

-- Add the python script that will compute the playcounts:
add file hdfs:///functions/generate_playcounts.py;

-- And a TSV file containing data similar to the semantic
-- analysis we did in lab #4
add file hdfs:///functions/word_scores.tsv;

-- Now run a map-only Hive query that uses the playcounts script 
-- to generate the playcounts from the bleats and the log files.

INSERT OVERWRITE TABLE BLEATS_INPUT 
SELECT user, artist, playcount
FROM (SELECT TRANSFORM(id, bleats, requests)
      USING 'generate_playcounts.py' 
      AS user, artist, playcount
      FROM SESSIONS) generated_playcounts;
