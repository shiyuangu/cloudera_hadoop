-- run the select on the access log table
SELECT
  COUNT(*)
FROM ACCESS_LOGS
  WHERE ip_address IS NULL
  OR date_string IS NULL
  OR request IS NULL
  OR bytes IS NULL
  OR referer IS NULL
  OR user_agent IS NULL
  OR cookie IS NULL;
