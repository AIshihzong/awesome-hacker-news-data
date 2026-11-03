# Awesome Hacker News Data（中文）

基于 Hacker News 全站存档的项目、数据集、查询和结论合集。**每个条目都标注了数据实际从哪来**，
方便你分辨哪些项目共用同一条数据管线、哪些可以自己复现。

[English](README.md) · [数据质量说明](DATA_QUALITY.md) · [查询库](queries/) · [派生数据](data/)

2026 年 10 月底，Karpathy 从 4300 万条 HN 评论里筛出 6,454 个被反复推荐的视频，做成了
[HackerTube](https://hackertube.org)。两天之内，书、论文、博客、播客、Wikipedia 条目、工具、
仓库的「HackerTube 版」全都冒了出来，大多数用的是 Hugging Face 上同一份 Parquet 存档。

## 数据来源标签

| 标签 | 含义 |
|---|---|
| `open-index` | 项目的 README、网站或作者说明使用了 [open-index/hacker-news](https://huggingface.co/datasets/open-index/hacker-news) |
| `HackerTube data` | 基于 [HackerTube 公开的导出数据](https://hackertube.org/data)，不是原始存档 |
| `Algolia API` · `HN API` · `BigQuery` | 查询的是实时数据源，不是这份存档 |
| `not stated` | 没找到数据来源，欢迎补充 |

## 快速开始

不用下载，在 [DuckDB](https://duckdb.org) 里直接查：

```sql
INSTALL httpfs; LOAD httpfs; SET TimeZone = 'UTC';
SELECT year(time) AS yr, count(*) AS comments
FROM 'hf://datasets/open-index/hacker-news/data/2025/*.parquet'
WHERE type = 2
GROUP BY yr;
```

正式分析前先运行 [`queries/00_setup.sql`](queries/00_setup.sql)。它会建好 `stories`、`comments`
两个视图，一个已经剔除坏月份的 `scored_stories` 视图，以及解码 HTML 的 `plain()` 宏。
想离线查询，可以用 [`scripts/build_local_db.py`](scripts/build_local_db.py) 建一个不含评论正文、
约 1.1 GB 的本地库。

## 先读这个：数据质量

详见 [DATA_QUALITY.md](DATA_QUALITY.md)。会改变结论的有三条：

1. **25 个月的分数被冻结**：2012-04、2012-11、2012-12、2013-02、2022-12 至 2023-12，以及 2026
   年至今。这些月份里达到 100 分的帖子不到 0.1%，正常月份是 3–6%。凡是用到分数的指标都要剔除它们。
2. **存档已停止更新**：最后一条数据是 2026-08-21，数据集最后一次发布是 2026-08-23。
3. **`time` 是带时区的时间戳**：先设 `TimeZone = 'UTC'`，否则年份和小时会按你的本地时区计算。

## 「HackerTube for X」类网站

套路都一样：从评论里提取某类链接，按「有多少不同的人贴过」排序。
[`queries/02_link_mining.sql`](queries/02_link_mining.sql) 实现了这个通用写法。

| 网站 | 排的是什么 | 数据来源 |
|---|---|---|
| [HackerTube](https://hackertube.org) | YouTube 视频 | `open-index` |
| [HackerBooks](https://hackerbooks.org) | 书（约 1.65 万本） | `not stated` |
| [Wikihack](https://wikihack.netlify.app) | Wikipedia 条目 | `not stated` |
| [Hacker Papers](https://academy.dair.ai/papers/collections/hacker-papers) | arXiv 论文 | `not stated` |
| [HackerBlogs (.app)](https://hackerblogs.app) | 博客 | `not stated` |
| [HackerBlogs (.org)](https://www.hackerblogs.org) | 博客和订阅源 | `open-index` |
| [HN AI Tools](https://hnaitools.dev) | AI 工具 | `open-index` + `Algolia API` |
| [Hacker Storytelling](https://hackerstorytelling.org) | 讲故事、写故事的话题 | `open-index` |
| [HackerPods](https://hackerpods.tiktalk.ing) | 播客 | `Algolia API` |
| [ShowReel](https://showreel-hn.netlify.app) | Show HN 产品演示 | `Algolia API` |
| [Hackertools](https://shouvik12.github.io/hackertools) | 开发者工具 | `Algolia API` |
| [hnrepos.com](https://hnrepos.com) | GitHub 仓库 | `BigQuery` |
| [HackerHype](https://epestr.com/hackerhype/) | 这类网站本身的索引 | `not stated` |

完整列表，包括客户端、移植版、搜索工具、基础设施和研究项目，见[英文 README](README.md)。
中文相关的有 [hackerbooks-zh](https://github.com/turygo/hackerbooks-zh)（HackerBooks 中文镜像，附豆瓣链接）
和 [hackertube-zh](https://github.com/bockybocky/hackertube-zh)（繁体中文版 HackerTube）。

## 二十年的数字

基于全量存档计算，凡是依赖分数的指标都已剔除冻结月份。

- 1% 的评论者写了 **55.4%** 的评论。
- 2008 年首次评论的人，有 43.3% 第二年还在评论。2024 年的新人只有 **16.0%**。
- 平均评论长度从 2016 年的 401 个字符降到 2026 年的 **337**。被处理（dead）的评论比例从 1.25% 升到 **3.92%**。
- 2015 年以来，Launch HN 有 **44%** 达到 100 分，普通链接 4.9%，Ask HN 2.8%。
- 2018 年以来，标题带年份（如「(2009)」）的帖子有 **9.4%** 达到 100 分，所有链接平均是 5.1%。
- 2020 年以来，最好的发帖时间是**周日 UTC 11 点**（7.6%）。
- 标题含 AI 词的帖子占比：2016 年 0.85%，2024 年 10.4%，2026 年 **21.0%**。
- Show HN 从 2022 年的 10,119 篇涨到 2025 年的 28,389 篇，达到 100 分的比例从 6.1% 跌到 **2.5%**，
  2025 年有 62% 的 Show HN 一条评论都没有。
- 2019 年之后，HN 上几乎看不到 Product Hunt 链接，从每年约 300 条降到个位数。

## 参与贡献

欢迎提 PR，规则见 [CONTRIBUTING.md](CONTRIBUTING.md)。每个条目需要：能打开的链接、一句话说明，
以及有据可查的数据来源标签。

## 许可

列表、查询和脚本采用 [CC0](LICENSE)。派生数据沿用源数据集的 ODC-By 许可。HN 内容的权利属于各自作者。
