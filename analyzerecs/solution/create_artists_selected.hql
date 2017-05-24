DROP TABLE IF EXISTS artists_selected;

-- Filter the recs logs to just be the user ID and the artist 
-- they added, and then group them by user id so that we have 
-- all of the artists a user added in a single row.
CREATE TABLE ARTISTS_SELECTED
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t' 
COLLECTION ITEMS TERMINATED BY '|'
AS
SELECT cookie as user,
collect_set(regexp_extract(request, "GET /listenArtist\\?id=(\\d+) HTTP/1.1", 1)) as artists
FROM RECS_LOGS
WHERE regexp_extract(request, "GET /listenArtist\\?id=(\\d+) HTTP/1.1", 1) != ""
GROUP BY cookie;

