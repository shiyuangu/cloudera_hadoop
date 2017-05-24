DROP TABLE IF EXISTS WORD_PLAYCOUNT_COUNTS;

CREATE TABLE WORD_PLAYCOUNT_COUNTS (word string, playcount int, count int)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

add file hdfs:///functions/extract_words_and_playcounts.py;

INSERT OVERWRITE TABLE WORD_PLAYCOUNT_COUNTS 
SELECT word, playcount, count(*) cnt
FROM (SELECT TRANSFORM(bleats, requests) USING 'extract_words_and_playcounts.py'
      AS word, playcount
      FROM SESSIONS) extracted_word_playcounts
GROUP BY word, playcount;

