-- Run this first in any DuckDB session (CLI, Python, or the WASM shell).
-- It reads the open-index/hacker-news Parquet files straight from Hugging Face; nothing is downloaded up front.
INSTALL httpfs;
LOAD httpfs;
SET TimeZone = 'UTC';  -- `time` is TIMESTAMPTZ; without this, years and hours come out in your local zone

-- Full archive: 239 monthly files, about 12 GB. Full scans take minutes, so start with one year.
CREATE OR REPLACE VIEW hn AS
SELECT * FROM read_parquet('hf://datasets/open-index/hacker-news/data/*/*.parquet');
-- CREATE OR REPLACE VIEW hn AS SELECT * FROM read_parquet('hf://datasets/open-index/hacker-news/data/2025/*.parquet');

-- type: 1 story, 2 comment, 3 poll, 4 poll option, 5 job. `by` is a reserved word, so quote it: "by".
CREATE OR REPLACE VIEW stories AS
SELECT *, strftime(time, '%Y-%m') AS month,
       lower(regexp_replace(regexp_extract(url, 'https?://([^/:]+)', 1), '^www\.', '')) AS domain
FROM hn WHERE type = 1 AND deleted = 0 AND dead = 0 AND title <> '';

CREATE OR REPLACE VIEW comments AS
SELECT * FROM hn WHERE type = 2 AND deleted = 0 AND text IS NOT NULL;

-- Months whose scores/descendants were frozen at ingest time (see DATA_QUALITY.md).
-- Filter on this before any score-based metric.
CREATE OR REPLACE TABLE frozen_months AS SELECT unnest([
  '2012-04', '2012-11', '2012-12', '2013-02',
  '2022-12', '2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06', '2023-07',
  '2023-08', '2023-09', '2023-10', '2023-11', '2023-12',
  '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07', '2026-08'
]) AS month;

CREATE OR REPLACE VIEW scored_stories AS
SELECT * FROM stories WHERE month NOT IN (SELECT month FROM frozen_months);

-- Comment and story text is HTML: tags plus entities such as &#x2F; (/), &#x27; ('), &quot; and &gt;.
CREATE OR REPLACE MACRO plain(t) AS
  replace(replace(replace(replace(replace(replace(replace(
    regexp_replace(t, '<[^>]+>', ' ', 'g'),
    '&#x2F;', '/'), '&#x27;', ''''), '&quot;', '"'), '&gt;', '>'), '&lt;', '<'), '&#x60;', '`'), '&amp;', '&');
