DROP TABLE IF EXISTS experiment_data;

-- Join the mixer logs data and the artists selected data on the user ID.
CREATE TABLE EXPERIMENT_DATA
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t' 
COLLECTION ITEMS TERMINATED BY '|'
AS
SELECT a.user, a.artists, b.entry as mixer_data
FROM ARTISTS_SELECTED a JOIN MIXER_LOGS b
ON (a.user = get_json_object(b.entry, '$.user_id'));

