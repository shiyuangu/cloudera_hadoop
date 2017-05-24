-- Number of users between 20 and 29 years old
select count(*) from sessions where age >=20 and age <=29;

-- Number of users who are female and over the age of 40
select count(*) from sessions where gender = 'F' and age >=40;

-- Californians
select count(*) from sessions where zipcode >= 90000 and zipcode <= 96199;

-- Number of sessions by gender
select gender, count(*) from sessions group by gender;

-- Users with the most bleats
select id, size(bleats) as numbleats from sessions order by numbleats desc limit 3;
