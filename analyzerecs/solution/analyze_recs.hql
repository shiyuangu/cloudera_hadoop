-- Analyze the experiment data using the interleaved.py script, 
-- and then get the aggregate counts of which recommendation 
-- algorithm the user preferred: A, B, or neither.
add file hdfs:///functions/interleaved.py;

SELECT pref, count(*)
  FROM (
    FROM EXPERIMENT_DATA
    SELECT TRANSFORM(user, artists, mixer_data) USING 'interleaved.py' AS pref) p
GROUP BY pref;
