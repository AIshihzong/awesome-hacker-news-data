-- Reproduce the frozen-score list: months where almost no story ever reached 100 points.
-- In normal months 3-6% of stories reach 100, while frozen months sit near 0% because scores were captured minutes after posting.
SELECT month,
       count(*) AS stories,
       round(avg((score >= 100)::INT) * 100, 2) AS pct_100_plus,
       round(avg(score), 2) AS avg_score
FROM stories
WHERE month >= '2012-01'
GROUP BY month
HAVING avg((score >= 100)::INT) < 0.03
ORDER BY month;
