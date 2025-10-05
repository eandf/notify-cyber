-- SELECT pg_size_pretty(pg_database_size('postgres'));

SELECT pg_size_pretty(pg_database_size('postgres')) AS database_size,
       COUNT(*) AS total_rows
FROM cybernews;

