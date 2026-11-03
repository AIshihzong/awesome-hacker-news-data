-- Which sites reliably make the front page? Share of submissions reaching 100 points, by domain, 2018+.
SELECT domain,
       count(*) AS submissions,
       round(avg((score >= 100)::INT) * 100, 1) AS pct_100_plus
FROM scored_stories
WHERE year(time) >= 2018 AND domain <> ''
GROUP BY domain
HAVING count(*) >= 300
ORDER BY pct_100_plus DESC
LIMIT 30;
