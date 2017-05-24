!sh echo Count of rows with null values in bleats table;
SELECT
  COUNT(*)
FROM BLEATS
  WHERE bleat IS NULL;

!sh echo Count of rows with null values in artist table;
SELECT
  COUNT(*)
FROM ARTIST
  WHERE id IS NULL
  OR name IS NULL
  OR year IS NULL;

!sh echo Count of rows with null values in users table;
SELECT
  COUNT(*)
FROM USERS
  WHERE id IS NULL
  OR gender IS NULL
  OR age IS NULL
  OR occupation IS NULL
  OR zipcode IS NULL;

