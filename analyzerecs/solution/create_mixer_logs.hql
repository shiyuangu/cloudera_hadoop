DROP TABLE IF EXISTS mixer_logs;

-- Load the mixer log JSON records.
CREATE EXTERNAL TABLE MIXER_LOGS (
  entry string
) 
LOCATION '/earcloud/mixerlogs';
