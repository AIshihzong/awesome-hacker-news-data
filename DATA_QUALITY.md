# Data quality notes for open-index/hacker-news

These notes come from loading all 239 monthly files of
[open-index/hacker-news](https://huggingface.co/datasets/open-index/hacker-news) into DuckDB
and checking them month by month. Read them before you publish a number.

## Coverage

| | |
|---|---|
| First item | 2006-10-09 |
| Last item | 2026-08-21 |
| Files | 239 monthly Parquet files, about 12 GB |
| Stories (`type = 1`) | 6,236,741 |
| Comments (`type = 2`) | 43,051,020 |
| Distinct commenters | 839,706 |
| Updates | **Stopped.** The dataset was last published on 2026-08-23. |

If you need anything after August 2026, combine it with a live source: the
[official HN API](https://github.com/HackerNews/API), the
[Algolia HN Search API](https://hn.algolia.com/api), or the
[BigQuery public dataset](https://console.cloud.google.com/marketplace/product/y-combinator/hacker-news).

## 1. Scores and comment counts are frozen in 25 months

In these months `score` and `descendants` were captured shortly after posting and never
updated. Nearly every story sits at a handful of points:

```
2012-04  2012-11  2012-12  2013-02
2022-12  2023-01 … 2023-12          (13 months)
2026-01 … 2026-08                   (8 months)
```

In a normal month 3–6% of stories reach 100 points. In these months the share is below 0.1%:
2026-06 has 0.08%, 2026-07 has 0.06% and 2026-08 has 0.05%.

**What this breaks:** any score-based metric such as top stories, win rates, best posting time or
"did HN get less generous?" that includes those months. It also breaks every score-based metric
for 2023 and 2026 as whole years. Story and comment *counts* are fine. Only `score` and
`descendants` are affected.

**Fix:** exclude the months. `queries/00_setup.sql` defines `frozen_months` and a
`scored_stories` view that already leaves them out. `queries/01_frozen_score_months.sql`
re-derives the list. It flags any month since 2012 where under 3% of stories reached 100 points.

## 2. Timestamps are `TIMESTAMPTZ`

`time` is stored with a time zone. DuckDB shows it, and computes `year()`, `hour()` and
`strftime()`, in your session's local zone. Run `SET TimeZone = 'UTC';` first, or items near
midnight land in the wrong day, month or year.

## 3. Text is HTML

`text` and some titles contain tags (`<p>`, `<a href=…>`, `<i>`) and entities such as `&#x2F;`
for `/`, `&#x27;` for `'`, `&quot;` and `&gt;`. Regexes that look for `https://` inside comments
miss links unless you decode `&#x2F;` first. `00_setup.sql` defines a `plain(text)` macro for
this.

## 4. Smaller gotchas

- `by` is a reserved word in SQL. Write it as `"by"`.
- `type`: 1 story, 2 comment, 3 poll, 4 poll option, 5 job.
- `dead` and `deleted` are `0`/`1` integers, not booleans. Deleted items have no author or text
  (about 951k comments). Dead items usually keep their text (89% of 839k dead comments do).
- `descendants` counts all comments in the thread. `kids` lists direct replies only.
- For Ask HN and other text posts, `url` is an empty string, not `NULL`. Extract the domain with
  `regexp_extract(url, 'https?://([^/:]+)', 1)` and strip `www.`.
