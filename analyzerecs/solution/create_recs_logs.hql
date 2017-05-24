DROP TABLE IF EXISTS recs_logs;

-- Load the recommendation logs file as an external table.
-- Note that all types must be strings for the regex serde
-- we do casts to tie fields together.
CREATE EXTERNAL TABLE RECS_LOGS (
  ip_address string, 
  date_string string, 
  request string, 
  response string, 
  bytes string, 
  referer string, 
  user_agent string, 
  cookie string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe' 
WITH SERDEPROPERTIES
(
"input.regex" = "^([\\d.]+) \\S+ \\S+ \\[(.+?)\\] \\\"(.+?)\\\" (\\d{3}) (\\d+) \\\"(.+?)\\\" \\\"(.+?)\\\" \\\"USER=(\\d+)\\\"\\s*"
) 
LOCATION '/earcloud/reclogs';
