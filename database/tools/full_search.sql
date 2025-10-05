PREPARE
  search_query (text) AS
SELECT
  *
FROM
  public.cybernews
WHERE
  url ILIKE '%' || $1 || '%'
  OR title ILIKE '%' || $1 || '%'
  OR details ILIKE '%' || $1 || '%';
EXECUTE
  search_query ('cve');

