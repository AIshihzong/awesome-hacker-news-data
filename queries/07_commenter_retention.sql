-- Of the people who first commented in year N, what share commented again in year N+1?
WITH active AS (
  SELECT "by" AS person, year(time) AS yr FROM comments WHERE "by" <> '' GROUP BY ALL
), cohort AS (
  SELECT person, min(yr) AS first_year FROM active GROUP BY person
)
SELECT c.first_year,
       count(*) AS new_commenters,
       CASE WHEN c.first_year < (SELECT max(yr) FROM active)
            THEN round(avg((a.person IS NOT NULL)::INT) * 100, 1) END AS pct_back_next_year
FROM cohort c
LEFT JOIN active a ON a.person = c.person AND a.yr = c.first_year + 1
GROUP BY c.first_year
ORDER BY c.first_year;
