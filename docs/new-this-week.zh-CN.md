# 本周新增

[English](new-this-week.md) · **简体中文** · [返回合集](../README.zh-CN.md)

每周新增和更正的条目，最新的在前。同样的内容会作为[周报](https://github.com/AIshihzong/awesome-hacker-news-data/releases)发布：**Watch → Custom → Releases** 即可订阅。

## 2026-11-03：第一次审核候选队列

逐个核对出处后新增 26 个项目和 1 个数据集，合集现在有 76 个项目、9 个数据集。

- **新的「HackerTube for X」**：[hackerrepos](https://jatingargiitk.github.io/hackerrepos/) 排了 29,109 个 GitHub 仓库，[DesignerTube](https://www.designertube.app) 选出 1,153 个给设计师看的视频，[PsychTube](https://github.com/contofalskyR/PsychTube) 做的是心理学，还有[另一个 HackerBooks](https://hacker-books-ecru.vercel.app) 用 Algolia API 排出 1,800 本书。
- **HackerTube 上了各种屏幕**：三星、LG、Fire TV 电视应用，原生 Android 和 iOS 应用，以及两个把 HN 推荐直接放进 YouTube 的 Chrome 扩展。
- **改了规则的重建版**：[markokovac16/hackertube](https://github.com/markokovac16/hackertube) 要求至少 8 人、跨 3 年推荐；[HacKiroTube](https://github.com/sanjayvs-shellkode/HacKiroTube) 会去找已删除视频的重新上传版本。
- **又多了三个中文版 HackerBooks**，以及中英双语的视频主题地图 [Offbranch](https://thesybuilder.github.io/offbranch/)。
- **新数据集**：[OpenPipe/hacker-news](https://huggingface.co/datasets/OpenPipe/hacker-news)。[cheap-hackertube](https://github.com/saqibns/cheap-hackertube) 用它测试：简单的频次统计能不能替代 HackerTube 的 LLM 筛选。
- `HackerTube data` 标签现在也包括读取 HackerTube 公开 JSON API 的应用。

没有收录的：数据镜像、个人副本、空仓库，以及只借用名字、没用 HN 数据的项目。

## 2026-11-03 这一周：第一期

合集上线，收录 50 个项目和 8 个数据集，每个都标注了实际用的数据。HackerTube 热潮第一周的重点：

- [HackerTube](https://hackertube.org) 于 2026-10-31 发布，在 HN 上拿到 [2,841 分](https://news.ycombinator.com/item?id=50319510)。`open-index`
- 一天后 [HackerBooks](https://hackerbooks.org) 跟进，收录约 1.65 万本书，拿到 [1,829 分](https://news.ycombinator.com/item?id=50326821)。`not stated`
- [Wikihack](https://wikihack.netlify.app) 做了 Wikipedia 条目版，[338 分](https://news.ycombinator.com/item?id=50333339)。`not stated`
- HackerTube 上了电视：Apple TV 版 [Jnaina/hackertube-tvos](https://github.com/Jnaina/hackertube-tvos)，Android TV 版 [hackertube.tv](https://github.com/ephraimduncan/hackertube.tv)。
- [HackerHype](https://epestr.com/hackerhype/) 开始收录这些 Hacker* 网站本身；也有人在 [Ask HN](https://news.ycombinator.com/item?id=50336496) 上问：大家不担心这波跟风吗？

仓库里也新增了[按数据来源分组的索引](by-source.zh-CN.md)，以及给准备发帖的人看的
[Show HN 数据](../README.zh-CN.md#show-hn-还值得发吗数据怎么说)。

有漏掉的项目？[提交给我们](https://github.com/AIshihzong/awesome-hacker-news-data/issues/new?template=project.yml)。
