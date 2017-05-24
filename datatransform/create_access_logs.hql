-- Load the access0.log file as an external table.

-- Note that all types must be strings for the regex serde
DROP TABLE IF EXISTS ACCESS_LOGS;

CREATE EXTERNAL TABLE ACCESS_LOGS (
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
LOCATION '/earcloud/accesslogfixed';
