# Awesome Hacker News Data

Projects, datasets, queries and findings built on the full Hacker News archive. **Every entry
lists where its data actually comes from**, so you can tell which projects share a pipeline
and which ones you can reproduce.

[中文说明](README.zh-CN.md) · [Data quality notes](DATA_QUALITY.md) · [Query library](queries/) · [Derived data](data/)

In late October 2026 Andrej Karpathy built [HackerTube](https://hackertube.org) by filtering
43 million HN comments down to 6,454 videos people keep recommending. Within two days there was a
HackerTube for books, papers, blogs, podcasts, Wikipedia articles, tools and repos. Most of them
start from the same Parquet archive on Hugging Face. This list collects them, along with the
older tools, analyses and the gotchas you hit when you query the data yourself.

## Contents

- [Quick start](#quick-start)
- [Read this first: data quality](#read-this-first-data-quality)
- [Datasets and APIs](#datasets-and-apis)
- [The "HackerTube for X" sites](#the-hackertube-for-x-sites)
- [Apps, ports and translations](#apps-ports-and-translations)
- [Search, trends and exploration](#search-trends-and-exploration)
- [Infrastructure and tools](#infrastructure-and-tools)
- [Analysis and research](#analysis-and-research)
- [Query library](#query-library)
- [Twenty years in numbers](#twenty-years-in-numbers)
- [Contributing](#contributing)

**Data source labels**

| Label | Meaning |
|---|---|
| `open-index` | The project's README, site or author says it uses [open-index/hacker-news](https://huggingface.co/datasets/open-index/hacker-news) |
| `HackerTube data` | Built on [HackerTube's published export](https://hackertube.org/data), not the raw archive |
| `Algolia API` · `HN API` · `BigQuery` | Queries a live source instead of the archive |
| `not stated` | We could not find a source. Corrections welcome |

## Quick start

No download needed. In the [DuckDB](https://duckdb.org) CLI or Python:

```sql
INSTALL httpfs; LOAD httpfs; SET TimeZone = 'UTC';
SELECT year(time) AS yr, count(*) AS comments
FROM 'hf://datasets/open-index/hacker-news/data/2025/*.parquet'
WHERE type = 2
GROUP BY yr;
```

For real work, run [`queries/00_setup.sql`](queries/00_setup.sql) first. It defines `stories`,
`comments`, a `scored_stories` view that drops the broken months, and a `plain()` macro that
decodes HTML. To query offline, [`scripts/build_local_db.py`](scripts/build_local_db.py) builds a
1.1 GB local copy without comment text.

## Read this first: data quality

[DATA_QUALITY.md](DATA_QUALITY.md) has the details. The three that change results:

1. **Scores are frozen in 25 months**: 2012-04, 2012-11, 2012-12, 2013-02, 2022-12 through 2023-12, and all of
   2026 so far. Under 0.1% of stories in those months reach 100 points, against
   3–6% in normal months. Leave them out of any score-based metric.
2. **The archive stopped updating.** The last item is from 2026-08-21, and the dataset was last
   published on 2026-08-23.
3. **`time` is `TIMESTAMPTZ`.** Set `TimeZone = 'UTC'`, or years and hours shift to your local zone.

## Datasets and APIs

- [open-index/hacker-news](https://huggingface.co/datasets/open-index/hacker-news): every item from 2006-10 to 2026-08 as monthly Parquet files, about 12 GB, ODC-By. This is what most projects below use.
- [open-index/hacker-news-rss](https://huggingface.co/datasets/open-index/hacker-news-rss) and [open-index/hacker-news-text-search](https://huggingface.co/datasets/open-index/hacker-news-text-search): sibling datasets from the same publisher.
- [HackerTube data export](https://hackertube.org/data): the 6,454 videos, the comments that recommend them, related-video links and embeddings.
- [BigQuery `hacker_news` public dataset](https://console.cloud.google.com/marketplace/product/y-combinator/hacker-news): a SQL-queryable copy, reported in HN threads to be kept up to date.
- [ClickHouse example dataset](https://clickhouse.com/docs/getting-started/example-datasets/hacker-news): instructions for loading HN into ClickHouse.
- [Official HN API](https://github.com/HackerNews/API): Firebase, live, no key or rate limit.
- [Algolia HN Search API](https://hn.algolia.com/api): full-text search with date filters. Many small projects use it instead of the archive.
- [sytelus/HackerNewsData](https://github.com/sytelus/HackerNewsData): an older dump of all stories and comments up to May 2014.

## The "HackerTube for X" sites

Mine comments for links of one kind, then rank by how many different people posted them.
[`queries/02_link_mining.sql`](queries/02_link_mining.sql) implements that pattern.

| Site | Ranks | Data source | Notes |
|---|---|---|---|
| [HackerTube](https://hackertube.org) | YouTube videos | `open-index` | The original. Its 43M-comment count matches the archive's 43.05M |
| [HackerBooks](https://hackerbooks.org) | Books (~16.5k, 2+ commenters) | `not stated` | Data downloadable from its about page. [Show HN](https://news.ycombinator.com/item?id=50326821), 1,818 points |
| [Wikihack](https://wikihack.netlify.app) | Wikipedia articles | `not stated` | [Show HN](https://news.ycombinator.com/item?id=50333339), 334 points |
| [Hacker Papers](https://academy.dair.ai/papers/collections/hacker-papers) | arXiv papers (1k+) | `not stated` | By DAIR.AI. The page carries an ODC-By credit |
| [HackerBlogs (.app)](https://hackerblogs.app) | Blogs (9,434 from 10.7M links) | `not stated` | Follow blogs and export them to RSS |
| [HackerBlogs (.org)](https://www.hackerblogs.org) · [repo](https://github.com/thejulez/hackerblogs) | Blogs, with feeds | `open-index` | A separate project from the .app site |
| [HN AI Tools](https://hnaitools.dev) · [repo](https://github.com/DontFretBrett/hn-ai-tools) | AI tools | `open-index` + `Algolia API` | |
| [Hacker Storytelling](https://hackerstorytelling.org) | 382 storytelling topics | `open-index` | Per the [author's post](https://x.com/kjv_life/status/2117195122555142325) |
| [HackerShelf](https://github.com/IshankDev/hackershelf) | Books from 2024–26 comments | `open-index` | |
| [HackerShelf (Tri Vo)](https://x.com/coyotevn/status/2117306682074436012) | 407 books (5+ threads across 4+ years) | `Algolia API` | Same name as the entry above, different project |
| [HackerPods](https://hackerpods.tiktalk.ing) | Podcasts and episodes | `Algolia API` | Has a methodology page |
| [ShowReel](https://showreel-hn.netlify.app) | Show HN product demos | `Algolia API` | |
| [Hackertools](https://shouvik12.github.io/hackertools) | Developer tools | `Algolia API` | |
| [hnrepos.com](https://hnrepos.com) | GitHub repositories | `BigQuery` | |
| [HackerX](https://hackerx.nishachay.tech) | X posts (266 of 2,733 scored) | `not stated` | |
| [HackerTubes](https://hackertubes.com) | YouTube videos | `open-index` | |
| [HackTok](https://hacktok.org) · [repo](https://github.com/rorz/hacktok) | HackerTube videos as a vertical feed | `HackerTube data` | |
| [OpenTube](https://github.com/vishalmysore/OpenTube) | 185k videos, filtered and measured | `open-index` | Reports accuracy and cost per pipeline stage, and builds a knowledge graph. [Write-up](https://medium.com/@visrow/karpathy-built-hackertube-i-built-opentube-20-years-of-hn-videos-filtered-af763bd270f4) |
| [Most-recommended GitHub repos](https://x.com/digital_iot/status/2117182997229346974) | Repos, by distinct recommenders | `open-index` | An analysis thread with methodology, not a site |
| [HackerHype](https://epestr.com/hackerhype/) | The Hacker* sites themselves | `not stated` | An index of this whole genre |

More HackerTube rebuilds: [itsgg/hackytube](https://github.com/itsgg/hackytube),
[Syedomershah99/MyTube](https://github.com/Syedomershah99/MyTube),
[domijin/HackerTube](https://github.com/domijin/HackerTube) and
[denrase/hackertube](https://github.com/denrase/hackertube), all `open-index`.

## Apps, ports and translations

- [hackertube.tv](https://github.com/ephraimduncan/hackertube.tv): HackerTube for Android TV. `not stated`
- [Jnaina/hackertube-tvos](https://github.com/Jnaina/hackertube-tvos): HackerTube on Apple TV. `open-index`
- [Rushikeshh-patil/hackertube-tv](https://github.com/Rushikeshh-patil/hackertube-tv): an Apple TV browser with offline semantic search. `HackerTube data`
- [cq0206/HackerTube](https://github.com/cq0206/HackerTube): a desktop app and Chrome extension. `HackerTube data`
- [bockybocky/hackertube-zh](https://github.com/bockybocky/hackertube-zh): a Traditional Chinese static site. `HackerTube data`
- [turygo/hackerbooks-zh](https://github.com/turygo/hackerbooks-zh): a Chinese mirror of HackerBooks with verified Chinese titles and Douban links. `HackerBooks data`

## Search, trends and exploration

- [Hacker News Trends](https://hackernewstrends.com) · [upstash/hacker-trends](https://github.com/upstash/hacker-trends): search 45M posts and comments and chart any term over time. `open-index`
- [HN N-gram Viewer](https://hngram.com) · [jchook/hngram](https://github.com/jchook/hngram): word frequency over time, stored in ClickHouse. `open-index`
- [dacapoday/hn](https://github.com/dacapoday/hn): browse and query HN from the terminal with DuckDB. `open-index`
- [hn.persona](https://hn-persona.vercel.app) · [xydac/hn-persona](https://github.com/xydac/hn-persona): profile any user's posting patterns, interests and writing style. `open-index`
- [ziahamza/parle-extension](https://github.com/ziahamza/parle-extension): a browser extension that shows what HN, Reddit and X said about the page you are on. `open-index`
- [amterp/amber](https://github.com/amterp/amber): resurface the best HN content from any past period. `Algolia API`
- [Querying Hacker News with DuckDB](https://ssp.sh/brain/querying-hackernews-with-duckdb-directly/): HackerTube, HackerBooks and Wikihack rebuilt as three queries, with an in-browser runner. `open-index`
- [Searching all of HN on a laptop](https://discuss.ai.google.dev/t/searching-all-of-hacker-news-with-embeddinggemma-2-on-a-laptop-49-3m-items-5-3-gb/196641): 49.3M items in one 5.34 GB EmbeddingGemma index. `not stated`

## Infrastructure and tools

- [tamnd/hn-fdw](https://github.com/tamnd/hn-fdw): query the full archive from Postgres through `duckdb_fdw`, without copying any data. By the dataset's author. `open-index`
- [nyacg/pagedb](https://github.com/nyacg/pagedb): a 100 GB live-synced database in one Cloudflare Durable Object, with an HN demo that has title and semantic search. `open-index`
- [huggingface/hf-mount](https://github.com/huggingface/hf-mount): mount Hugging Face repos as local filesystems. Its README uses this dataset as the example. `open-index`
- [davanstrien/uv-scripts › build-atlas](https://github.com/davanstrien/uv-scripts/tree/main/build-atlas): prepares HN for an embedding atlas. `open-index`
- [credibledata/hackernews-demo](https://github.com/credibledata/hackernews-demo): ask natural-language questions through a Malloy semantic model. `open-index`
- [stevemurr/windex](https://github.com/stevemurr/windex): a self-hosted web index for search agents, with HN as one source. `open-index`
- [iannuttall/hn-get](https://github.com/iannuttall/hn-get): one HN pipeline for CLI, MCP, HTTP and RSS. `Algolia API` + `HN API`

## Analysis and research

- [zaporter/hacker-news-quality](https://github.com/zaporter/hacker-news-quality): an LLM scores comments from 2015–2026 to test whether HN quality has really declined. `open-index`
- [malakhov-dmitrii/hackernews-simulator](https://github.com/malakhov-dmitrii/hackernews-simulator): predicts a post's score and simulates its comments before you submit. `open-index`
- [kevinw-openai/hackernews-openclaw-analysis](https://github.com/kevinw-openai/hackernews-openclaw-analysis): a single-topic trend report with a browsing UI. `open-index`
- [google-research › dp_clip](https://github.com/google-research/google-research/tree/master/dp_clip): differential-privacy research that loads HN as a sparse user-by-thread matrix. `open-index`
- [Reverse-engineering the HN ranking algorithm](https://github.com/sangaline/reverse-engineering-the-hacker-news-ranking-algorithm): a 2017 analysis of historical front-page data.

## Query library

Every query runs against the Hugging Face files directly. Run [`00_setup.sql`](queries/00_setup.sql)
first. Full-archive scans take minutes, and `00_setup.sql` shows how to start with one year.

| Query | Answers |
|---|---|
| [01_frozen_score_months](queries/01_frozen_score_months.sql) | Which months have unusable scores? |
| [02_link_mining](queries/02_link_mining.sql) | The HackerTube pattern for any kind of link |
| [03_show_hn_trend](queries/03_show_hn_trend.sql) | Show HN volume and the odds of reaching 100 points, by year |
| [04_domain_win_rate](queries/04_domain_win_rate.sql) | Which sites reliably reach the front page |
| [05_demand_phrases](queries/05_demand_phrases.sql) | "I'd pay for…", "I wish there was…", "is there a tool…" |
| [06_posting_time](queries/06_posting_time.sql) | Best weekday and UTC hour to post |
| [07_commenter_retention](queries/07_commenter_retention.sql) | How many new commenters come back the next year |

## Twenty years in numbers

Computed from the full archive, with frozen months excluded wherever a number depends on scores.
The yearly series are in [`data/`](data/).

**The community**
- 1% of commenters write **55.4%** of all comments.
- 43.3% of people who first commented in 2008 commented again in 2009. For the 2024 cohort that
  share was **16.0%**.
- The average comment shrank from 401 characters in 2016 to **337** in 2026. The share of dead
  comments rose from 1.25% to **3.92%**.
- Comments per story peaked at 13.2 in 2022 and were 11.5 in 2025.

**What gets upvoted**
- Since 2015, Launch HN posts have reached 100 points **44%** of the time, ordinary links 4.9% and
  Ask HN 2.8%.
- Since 2018, titles with a year in brackets, such as "(2009)", reach 100 points **9.4%** of the time, against
  5.1% for all links. Titles under 15 characters do 6.6%, and 60+ characters about 4.6%.
- The best slot from 2020 on is **Sunday 11:00 UTC**, at 7.6%.
- By domain since 2018, blog.ycombinator.com leads at 23.2%, then jvns.ca at 22.1% and hacks.mozilla.org at
  21.1%. medium.com manages 1.4% across 51,131 submissions.

**The AI and Show HN wave**
- AI terms appeared in 0.85% of story titles in 2016, 10.4% in 2024 and **21.0%** in 2026. In
  2025, AI stories reached 100 points 3.2% of the time, against 4.8% for everything else.
- Show HN went from 10,119 posts in 2022 to 28,389 in 2025, and 32,616 in just the first eight
  months of 2026. The share reaching 100 points fell from 6.1% to **2.5%**, and 62% of 2025 Show HN
  posts got no comments at all.
- Product Hunt links almost vanished from HN after 2019, from about 300 a year to single digits.

## Derived data

[`data/`](data/) holds small CSVs computed from the archive: yearly metrics, monthly story counts
with a `scores_usable` flag, commenter cohorts, domain win rates, Show HN by year, and sampled
demand-phrase counts. They inherit the source's
[ODC-By](https://opendatacommons.org/licenses/by/1-0/) attribution requirement. Credit
open-index/hacker-news and Hacker News.

## Contributing

Add a project with a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md). Each entry needs a
working link, one line on what it does, and a data source label backed by something you can point
to.

## License

The list, queries and scripts are [CC0](LICENSE). The derived data follows the source dataset's
ODC-By license. Hacker News content belongs to its authors.
