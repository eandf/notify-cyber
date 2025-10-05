WITH DuplicateUrls AS (
    SELECT url
    FROM public.cybernews
    GROUP BY url
    HAVING COUNT(*) > 1
)
SELECT cn.id, cn.url, COUNT(*) OVER (PARTITION BY cn.url) AS total_rows
FROM public.cybernews cn
JOIN DuplicateUrls d ON cn.url = d.url;

-- SELECT url, COUNT(*) AS total_rows
-- FROM public.cybernews
-- GROUP BY url
-- HAVING COUNT(*) > 1;

-- SELECT url, COUNT(*) AS total_rows, STRING_AGG(CAST(id AS text), ', ') AS ids
-- FROM public.cybernews
-- GROUP BY url
-- HAVING COUNT(*) > 1;

-- SELECT COUNT(*) AS total_duplicate_rows
-- FROM (
--     SELECT url, COUNT(*) AS row_count
--     FROM public.cybernews
--     GROUP BY url
--     HAVING COUNT(*) > 1
-- ) AS subquery;
