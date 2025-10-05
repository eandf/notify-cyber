SELECT interval_month AS "months_ago", AVG(daily_count) AS average_per_day
FROM (
  SELECT
    1 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '1 month'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    2 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '2 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    3 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '3 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    4 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '4 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    5 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '5 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    6 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '6 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    7 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '7 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    8 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '8 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    9 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '9 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    10 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '10 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    11 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '11 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    12 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '12 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    13 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '13 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    14 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '14 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    15 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '15 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    16 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '16 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    17 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '17 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    18 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '18 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    19 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '19 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    20 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '20 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    21 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '21 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    22 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '22 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    23 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '23 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

  UNION ALL

  SELECT
    24 AS interval_month,
    COUNT(*) AS daily_count
  FROM cybernews
  WHERE TO_TIMESTAMP(recorded) >= NOW() - INTERVAL '24 months'
  GROUP BY DATE(TO_TIMESTAMP(recorded))

) AS monthly_counts
GROUP BY interval_month
ORDER BY interval_month;
