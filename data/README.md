# Derived data

Small aggregates computed from [open-index/hacker-news](https://huggingface.co/datasets/open-index/hacker-news)
(data through 2026-08-21). Score-based columns exclude the frozen months listed in
[DATA_QUALITY.md](../DATA_QUALITY.md). They are empty for years where too few months are usable.
Licensed ODC-By: credit open-index/hacker-news and Hacker News.

| File | Contents |
|---|---|
| `yearly.csv` | One row per year: volume, comment length, dead share, 100+ point rates, topic shares in titles, link-domain shares |
| `monthly_stories.csv` | Stories per month, share reaching 100 points, and `scores_usable` (false for frozen months) |
| `commenter_cohorts.csv` | New commenters per first-comment year, and the share active one and three years later |
| `domain_win_rates.csv` | 2018+ domains with the highest (300+ submissions) and lowest (2,000+) share reaching 100 points |
| `show_hn_yearly.csv` | Show HN posts per year, share reaching 100 points, share with no comments |
| `demand_signals_sampled.csv` | Counts of "I'd pay", "I wish there was", "is there a tool", "alternative to" and producthunt.com links in comments, sampled from four months a year (two in 2026) |

All `pct_*` columns are percentages from 0 to 100.
