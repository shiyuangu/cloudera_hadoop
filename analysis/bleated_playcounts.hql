DROP TABLE IF EXISTS BLEATED_PLAYCOUNTS;

CREATE TABLE BLEATED_PLAYCOUNTS (bleated int, playcount int, count int)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

add file hdfs:///functions/extract_playcounts.py;

INSERT OVERWRITE TABLE BLEATED_PLAYCOUNTS
SELECT bleated, playcount, count(*) cnt
FROM (SELECT TRANSFORM(bleats, requests) USING 'extract_playcounts.py'
      AS bleated, playcount
      FROM SESSIONS) extracted_playcounts
GROUP BY bleated, playcount;
