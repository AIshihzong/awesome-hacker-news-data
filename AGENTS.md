# AGENTS.md

Instructions for coding agents and AI assistants changing this list.

This repository is a **curated list with a small query library**, not a software project. Every
entry is a claim about someone else's work, and the list is only worth anything if those claims
can be checked. Read this before adding anything.

## The one rule that matters

**A data source label states what the project's own README, site or author says.** Do not infer
it. A site that looks like HackerTube is not `open-index` until its source says so. If you can't
find a statement, the label is `not stated`.

## Labels

| Label | Means | Evidence to look for |
|---|---|---|
| `open-index` | Uses the open-index/hacker-news archive | README, site or post naming the dataset or its `hf://` path |
| `HackerTube data` | Uses HackerTube's export or its JSON API | Mentions hackertube.org/data or calls hackertube.org/api |
| `HackerBooks data` | Uses HackerBooks' data | Mentions HackerBooks' download |
| `OpenPipe` | Uses the OpenPipe/hacker-news dump | Names the dataset |
| `Algolia API` | Calls hn.algolia.com | README or code calling the API |
| `HN API` | Calls the Firebase API | README or code calling hacker-news.firebaseio.com |
| `BigQuery` | Queries `bigquery-public-data.hacker_news` | README or code |
| `own data` | Collects and ships its own data | Data files in the repo, or a described crawl |
| `not stated` | Nothing found | |

Two labels are joined with ` + `, for example `` `open-index` + `Algolia API` ``.

## Where an entry goes

| Section | What belongs there |
|---|---|
| The "HackerTube for X" sites | Sites that rank one kind of link mined from comments |
| Apps, ports and translations | Clients, TV apps, extensions and translated mirrors of those sites |
| Search, trends and exploration | Tools for searching or charting HN itself |
| Infrastructure and tools | Loaders, databases and pipelines |
| Analysis and research | Write-ups, papers and one-off analyses |
| Datasets and APIs | Data sources, not projects |

## Format

A table row in the "HackerTube for X" table, or one bullet elsewhere:

```
- [owner/repo](link): what it does, with a number where you have one. `label`
```

## Before you open a pull request

1. Run `python3 scripts/validate_list.py --write` and commit the regenerated `docs/by-source*.md`.
   It must report 0 errors. It also checks that the counts in `assets/readme/hero*.svg` match the
   README. If you add a project, change the counts in `scripts/draw_hero.py` and run
   `python3 scripts/draw_hero.py assets/readme`.
2. If the project belongs in the Chinese table in `README.zh-CN.md`, add it there too.
3. Add a line to `docs/new-this-week.md` and `docs/new-this-week.zh-CN.md`.
4. Numbers that change, such as HN points or star counts, carry the date you checked them.
5. If you review a discovery candidate and leave it out, add it to `.github/discover-skip.txt`
   with the reason, so the daily search stops suggesting it.

## Queries

Changes to `queries/` must run after `00_setup.sql` on at least one month of data. Say which
month in the pull request. Read [DATA_QUALITY.md](DATA_QUALITY.md) first: scores are frozen in 25
months, `time` needs `SET TimeZone = 'UTC'`, and text is HTML.
