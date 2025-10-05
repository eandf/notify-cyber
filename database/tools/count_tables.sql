SELECT 
  COALESCE(grouped.source::VARCHAR, '-') AS source, 
  COALESCE(grouped.num_rows::INTEGER, 0) AS num_rows,
  COALESCE(overall.non_cve::INTEGER, 0) AS non_cve,
  COALESCE(overall.cve::INTEGER, 0) AS cve
FROM 
  (SELECT 
     source, 
     COUNT(*) AS num_rows
   FROM 
     cybernews
   GROUP BY 
     source) AS grouped
LEFT JOIN 
  (SELECT 
     SUM(CASE WHEN source != 'cve' THEN 1 ELSE 0 END) AS non_cve,
     SUM(CASE WHEN source = 'cve' THEN 1 ELSE 0 END) AS cve
   FROM 
     cybernews) AS overall
ON 
  grouped.source = 'cve' AND overall.cve = grouped.num_rows;

