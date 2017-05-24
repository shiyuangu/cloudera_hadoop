DROP TABLE IF EXISTS BLEATS;

-- Load the bleats data. 
CREATE EXTERNAL TABLE BLEATS 
(
  bleat string
)
LOCATION '/earcloud/bleats';
