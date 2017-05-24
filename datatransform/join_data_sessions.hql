DROP TABLE IF EXISTS SESSIONS;

-- To join all of the data we want together in a single step.
CREATE TABLE SESSIONS AS
SELECT a.id, age, gender, zipcode, collect_set(request) requests, collect_set(bleat) bleats
FROM USERS a
LEFT OUTER JOIN BLEATER_IDS b ON (a.id = b.user_id)
LEFT OUTER JOIN BLEATSFIXED c ON (b.bleater_id = get_json_object(c.bleat, '$.user.id'))
LEFT OUTER JOIN ACCESS_LOGS d ON (a.id = d.cookie)
GROUP BY a.id, age, gender, zipcode;
