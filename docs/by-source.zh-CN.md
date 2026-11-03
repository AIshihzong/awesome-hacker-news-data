# 按数据来源索引

[English](by-source.md) · **简体中文** · [返回合集](../README.zh-CN.md)

由 `scripts/validate_list.py --write` 根据英文 README 自动生成，请不要手动修改。同时使用两种来源的项目会在两组里都出现。

| 来源 | 项目数 |
|---|---:|
| [`open-index`](#open-index) | 29 |
| [`HackerTube data`](#hackertube-data) | 4 |
| [`HackerBooks data`](#hackerbooks-data) | 1 |
| [`Algolia API`](#algolia-api) | 7 |
| [`HN API`](#hn-api) | 1 |
| [`BigQuery`](#bigquery) | 1 |
| [`own data`](#own-data) | 1 |
| [`not stated`](#not-stated) | 8 |

## open-index

使用 [open-index/hacker-news](https://huggingface.co/datasets/open-index/hacker-news) 存档。

- [HackerTube](https://hackertube.org) · 「HackerTube for X」类网站
- [HackerBlogs (.org)](https://www.hackerblogs.org) · 「HackerTube for X」类网站
- [HN AI Tools](https://hnaitools.dev) · 「HackerTube for X」类网站
- [Hacker Storytelling](https://hackerstorytelling.org) · 「HackerTube for X」类网站
- [HackerShelf](https://github.com/IshankDev/hackershelf) · 「HackerTube for X」类网站
- [HackerTubes](https://hackertubes.com) · 「HackerTube for X」类网站
- [OpenTube](https://github.com/vishalmysore/OpenTube) · 「HackerTube for X」类网站
- [Most-recommended GitHub repos](https://x.com/digital_iot/status/2117182997229346974) · 「HackerTube for X」类网站
- [itsgg/hackytube](https://github.com/itsgg/hackytube) · 「HackerTube for X」类网站
- [Syedomershah99/MyTube](https://github.com/Syedomershah99/MyTube) · 「HackerTube for X」类网站
- [domijin/HackerTube](https://github.com/domijin/HackerTube) · 「HackerTube for X」类网站
- [denrase/hackertube](https://github.com/denrase/hackertube) · 「HackerTube for X」类网站
- [Jnaina/hackertube-tvos](https://github.com/Jnaina/hackertube-tvos) · 应用、移植和翻译
- [Hacker News Trends](https://hackernewstrends.com) · 搜索、趋势和探索
- [HN N-gram Viewer](https://hngram.com) · 搜索、趋势和探索
- [dacapoday/hn](https://github.com/dacapoday/hn) · 搜索、趋势和探索
- [hn.persona](https://hn-persona.vercel.app) · 搜索、趋势和探索
- [ziahamza/parle-extension](https://github.com/ziahamza/parle-extension) · 搜索、趋势和探索
- [Querying Hacker News with DuckDB](https://ssp.sh/brain/querying-hackernews-with-duckdb-directly/) · 搜索、趋势和探索
- [tamnd/hn-fdw](https://github.com/tamnd/hn-fdw) · 基础设施和工具
- [nyacg/pagedb](https://github.com/nyacg/pagedb) · 基础设施和工具
- [huggingface/hf-mount](https://github.com/huggingface/hf-mount) · 基础设施和工具
- [davanstrien/uv-scripts › build-atlas](https://github.com/davanstrien/uv-scripts/tree/main/build-atlas) · 基础设施和工具
- [credibledata/hackernews-demo](https://github.com/credibledata/hackernews-demo) · 基础设施和工具
- [stevemurr/windex](https://github.com/stevemurr/windex) · 基础设施和工具
- [zaporter/hacker-news-quality](https://github.com/zaporter/hacker-news-quality) · 分析和研究
- [malakhov-dmitrii/hackernews-simulator](https://github.com/malakhov-dmitrii/hackernews-simulator) · 分析和研究
- [kevinw-openai/hackernews-openclaw-analysis](https://github.com/kevinw-openai/hackernews-openclaw-analysis) · 分析和研究
- [google-research › dp_clip](https://github.com/google-research/google-research/tree/master/dp_clip) · 分析和研究

## HackerTube data

基于 [HackerTube 公开的导出数据](https://hackertube.org/data)。

- [HackTok](https://hacktok.org) · 「HackerTube for X」类网站
- [Rushikeshh-patil/hackertube-tv](https://github.com/Rushikeshh-patil/hackertube-tv) · 应用、移植和翻译
- [cq0206/HackerTube](https://github.com/cq0206/HackerTube) · 应用、移植和翻译
- [bockybocky/hackertube-zh](https://github.com/bockybocky/hackertube-zh) · 应用、移植和翻译

## HackerBooks data

基于 HackerBooks 提供下载的数据。

- [turygo/hackerbooks-zh](https://github.com/turygo/hackerbooks-zh) · 应用、移植和翻译

## Algolia API

调用实时的 [Algolia HN Search API](https://hn.algolia.com/api)。

- [HN AI Tools](https://hnaitools.dev) · 「HackerTube for X」类网站
- [HackerShelf (Tri Vo)](https://x.com/coyotevn/status/2117306682074436012) · 「HackerTube for X」类网站
- [HackerPods](https://hackerpods.tiktalk.ing) · 「HackerTube for X」类网站
- [ShowReel](https://showreel-hn.netlify.app) · 「HackerTube for X」类网站
- [Hackertools](https://shouvik12.github.io/hackertools) · 「HackerTube for X」类网站
- [amterp/amber](https://github.com/amterp/amber) · 搜索、趋势和探索
- [iannuttall/hn-get](https://github.com/iannuttall/hn-get) · 基础设施和工具

## HN API

调用实时的[官方 HN API](https://github.com/HackerNews/API)。

- [iannuttall/hn-get](https://github.com/iannuttall/hn-get) · 基础设施和工具

## BigQuery

查询 [BigQuery 公开数据集](https://console.cloud.google.com/marketplace/product/y-combinator/hacker-news)。

- [hnrepos.com](https://hnrepos.com) · 「HackerTube for X」类网站

## own data

自己采集并附带数据。

- [Reverse-engineering the HN ranking algorithm](https://github.com/sangaline/reverse-engineering-the-hacker-news-ranking-algorithm) · 分析和研究

## not stated

还没找到数据来源。如果你知道，[告诉我们](https://github.com/AIshihzong/awesome-hacker-news-data/issues/new?template=project.yml)。

- [HackerBooks](https://hackerbooks.org) · 「HackerTube for X」类网站
- [Wikihack](https://wikihack.netlify.app) · 「HackerTube for X」类网站
- [Hacker Papers](https://academy.dair.ai/papers/collections/hacker-papers) · 「HackerTube for X」类网站
- [HackerBlogs (.app)](https://hackerblogs.app) · 「HackerTube for X」类网站
- [HackerX](https://hackerx.nishachay.tech) · 「HackerTube for X」类网站
- [HackerHype](https://epestr.com/hackerhype/) · 「HackerTube for X」类网站
- [hackertube.tv](https://github.com/ephraimduncan/hackertube.tv) · 应用、移植和翻译
- [Searching all of HN on a laptop](https://discuss.ai.google.dev/t/searching-all-of-hacker-news-with-embeddinggemma-2-on-a-laptop-49-3m-items-5-3-gb/196641) · 搜索、趋势和探索
