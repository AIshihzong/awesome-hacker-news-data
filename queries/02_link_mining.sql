-- The HackerTube pattern, generalised: find links of one kind in comments and rank them by how many
-- different people posted them. Change link_pattern to mine books (openlibrary/amazon), papers (arxiv),
-- repos (github), Wikipedia, podcasts, ...
SET VARIABLE link_pattern = 'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})';
SET VARIABLE min_people = 3;

WITH hits AS (
  SELECT "by" AS person, year(time) AS yr, id,
         unnest(regexp_extract_all(plain(text), getvariable('link_pattern'), 1)) AS key
  FROM comments
)
SELECT key,
       count(DISTINCT person) AS people,
       count(DISTINCT yr) AS distinct_years,
       min(yr) AS first_year,
       max(yr) AS last_year,
       min(id) AS first_comment_id  -- https://news.ycombinator.com/item?id=<id>
FROM hits
GROUP BY key
HAVING count(DISTINCT person) >= getvariable('min_people')
ORDER BY people DESC
LIMIT 100;
