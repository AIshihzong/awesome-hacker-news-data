-- When do stories do best? Share reaching 100 points by weekday and UTC hour, 2020+.
SELECT isodow(time) AS weekday,  -- 1 = Monday
       hour(time) AS utc_hour,
       count(*) AS stories,
       round(avg((score >= 100)::INT) * 100, 2) AS pct_100_plus
FROM scored_stories
WHERE year(time) >= 2020
GROUP BY ALL
HAVING count(*) >= 1000
ORDER BY pct_100_plus DESC
LIMIT 20;
