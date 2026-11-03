-- Show HN volume vs. the chance of reaching 100 points, per year (frozen months excluded from the rate).
SELECT year(time) AS yr,
       count(*) AS show_hn_posts,
       round(avg((score >= 100)::INT) FILTER (WHERE month NOT IN (SELECT month FROM frozen_months)) * 100, 1) AS pct_100_plus,
       round(avg((descendants = 0)::INT) FILTER (WHERE month NOT IN (SELECT month FROM frozen_months)) * 100, 1) AS pct_no_comments
FROM stories
WHERE title ILIKE 'Show HN%'
GROUP BY yr
ORDER BY yr;
