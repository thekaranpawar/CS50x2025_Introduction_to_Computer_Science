-- Top 5 longest songs in descending order of length
SELECT name
FROM songs
ORDER BY duration_ms DESC
LIMIT 5;

