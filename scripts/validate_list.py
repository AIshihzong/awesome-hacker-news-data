"""Check the list and build docs/by-source*.md from README.md.

    python3 scripts/validate_list.py           # check, exit 1 on errors
    python3 scripts/validate_list.py --write   # also regenerate docs/by-source*.md

Checks:
  - every project entry carries known data source labels
  - the project and dataset counts in the hero images match the README
  - the table of contents and every #anchor point at a real heading
  - relative links point at files that exist
  - every project linked from README.zh-CN.md is also in README.md
  - docs/by-source.md and docs/by-source.zh-CN.md are up to date
"""
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LABELS = ["open-index", "HackerTube data", "HackerBooks data", "OpenPipe", "Algolia API", "HN API",
          "BigQuery", "own data", "not stated"]

# Sections of README.md that hold projects, with their Chinese names for the index page.
PROJECT_SECTIONS = {
    'The "HackerTube for X" sites': "「HackerTube for X」类网站",
    "Apps, ports and translations": "应用、移植和翻译",
    "Search, trends and exploration": "搜索、趋势和探索",
    "Infrastructure and tools": "基础设施和工具",
    "Analysis and research": "分析和研究",
}
DATASET_SECTION = "Datasets and APIs"

LABEL_TEXT = {
    "open-index": ("Uses the [open-index/hacker-news](https://huggingface.co/datasets/open-index/hacker-news) archive.",
                   "使用 [open-index/hacker-news](https://huggingface.co/datasets/open-index/hacker-news) 存档。"),
    "HackerTube data": ("Built on [HackerTube's published export](https://hackertube.org/data) or its public JSON API.",
                        "基于 [HackerTube 公开的导出数据](https://hackertube.org/data)或它的公开 JSON API。"),
    "HackerBooks data": ("Built on HackerBooks' downloadable data.", "基于 HackerBooks 提供下载的数据。"),
    "OpenPipe": ("Uses the [OpenPipe/hacker-news](https://huggingface.co/datasets/OpenPipe/hacker-news) dump, which ends in November 2023.",
                 "使用 [OpenPipe/hacker-news](https://huggingface.co/datasets/OpenPipe/hacker-news) 数据，截至 2023 年 11 月。"),
    "Algolia API": ("Calls the live [Algolia HN Search API](https://hn.algolia.com/api).",
                    "调用实时的 [Algolia HN Search API](https://hn.algolia.com/api)。"),
    "HN API": ("Calls the live [official HN API](https://github.com/HackerNews/API).",
               "调用实时的[官方 HN API](https://github.com/HackerNews/API)。"),
    "BigQuery": ("Queries the [BigQuery public dataset](https://console.cloud.google.com/marketplace/product/y-combinator/hacker-news).",
                 "查询 [BigQuery 公开数据集](https://console.cloud.google.com/marketplace/product/y-combinator/hacker-news)。"),
    "own data": ("Collects and ships its own data.", "自己采集并附带数据。"),
    "not stated": ("No source found yet. If you know it, [tell us](https://github.com/AIshihzong/awesome-hacker-news-data/issues/new?template=project.yml).",
                   "还没找到数据来源。如果你知道，[告诉我们](https://github.com/AIshihzong/awesome-hacker-news-data/issues/new?template=project.yml)。"),
}

LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
TICK = re.compile(r"`([^`]+)`")
TRAILING_LABELS = re.compile(r"((?:`[^`]+`(?: \+ )?)+)\.?$")

errors = []


def err(path, line, msg):
    errors.append(f"{path}:{line}: {msg}")


def sections(text):
    """Map each '## ' heading to its (first line number, lines)."""
    out, name, start, buf = {}, None, 0, []
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            if name:
                out[name] = (start, buf)
            name, start, buf = line[3:].strip(), i, []
        elif name:
            buf.append(line)
    if name:
        out[name] = (start, buf)
    return out


def check_labels(found, path, lineno):
    if not found:
        err(path, lineno, "entry has no data source label")
    for label in found:
        if label not in LABELS:
            err(path, lineno, f"unknown label `{label}`")


def parse_projects(path):
    """Return [(name, url, labels, section)] for every project in README.md."""
    projects = []
    for name, (start, lines) in sections(path.read_text()).items():
        if name not in PROJECT_SECTIONS:
            continue
        label_col = None
        for offset, line in enumerate(lines, 1):
            n = start + offset
            if line.startswith("|"):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if label_col is None:
                    label_col = cells.index("Data source") if "Data source" in cells else -1
                    continue
                if set(cells[0]) <= set("-: "):
                    continue
                link = LINK.search(cells[0])
                labels = TICK.findall(cells[label_col])
                check_labels(labels, path.name, n)
                projects.append((link.group(1), link.group(2), labels, name))
            elif line.startswith("- ["):
                link = LINK.search(line)
                m = TRAILING_LABELS.search(line)
                labels = TICK.findall(m.group(1)) if m else []
                check_labels(labels, path.name, n)
                projects.append((link.group(1), link.group(2), labels, name))
    return projects


def count_datasets(path):
    start, lines = sections(path.read_text())[DATASET_SECTION]
    return sum(line.startswith("- [") for line in lines)


def slug(heading):
    """GitHub's heading anchor."""
    h = heading.strip().lower()
    h = "".join(c for c in h if c in "-_ " or unicodedata.category(c)[0] in "LN")
    return h.replace(" ", "-")


def anchors(path):
    seen, out = defaultdict(int), set()
    in_code = False
    for line in path.read_text().splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        m = re.match(r"#{1,6} (.+)", line)
        if m:
            text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", m.group(1))
            text = re.sub(r"!?\[[^\]]*\]\([^)]*\)", "", text)
            s = slug(text.replace("`", ""))
            out.add(s if not seen[s] else f"{s}-{seen[s]}")
            seen[s] += 1
    return out


def check_links(path):
    text = path.read_text()
    own = anchors(path)
    in_code = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        targets = [u for _, u in LINK.findall(line)] + re.findall(r'(?:src|href)="([^"]+)"', line)
        for url in targets:
            if re.match(r"[a-z]+:", url):
                continue
            target, _, frag = url.partition("#")
            dest = (path.parent / target).resolve() if target else path
            if not dest.exists():
                err(path.relative_to(ROOT), n, f"broken relative link {url}")
            elif frag and dest.suffix == ".md" and frag not in anchors(dest):
                err(path.relative_to(ROOT), n, f"no heading for #{frag} in {dest.name}")
    return own


def check_toc(path):
    secs = sections(path.read_text())
    if "Contents" not in secs:
        return
    start, lines = secs["Contents"]
    listed = [m.group(1) for line in lines for m in [re.match(r"- \[[^\]]+\]\(#([^)]+)\)", line)] if m]
    following = [slug(h) for h in list(secs)[list(secs).index("Contents") + 1:]]
    for a in listed:
        if a not in following:
            err(path.name, start, f"contents lists #{a}, which is not a section after it")
    stop = slug("Contributing")
    for a in following[:following.index(stop) if stop in following else None]:
        if a not in listed:
            err(path.name, start, f"section #{a} is missing from the contents")


def by_source(projects, zh):
    groups = defaultdict(list)
    for name, url, labels, section in projects:
        for label in labels:
            groups[label].append((name, url, section))
    if zh:
        out = ["# 按数据来源索引", "",
               "[English](by-source.md) · **简体中文** · [返回合集](../README.zh-CN.md)", "",
               "由 `scripts/validate_list.py --write` 根据英文 README 自动生成，请不要手动修改。"
               "同时使用两种来源的项目会在两组里都出现。", ""]
    else:
        out = ["# Projects by data source", "",
               "**English** · [简体中文](by-source.zh-CN.md) · [Back to the list](../README.md)", "",
               "Generated from README.md by `scripts/validate_list.py --write`. Do not edit by hand. "
               "A project that uses two sources is listed under both.", ""]
    out.append("| Source | Projects |" if not zh else "| 来源 | 项目数 |")
    out.append("|---|---:|")
    for label in LABELS:
        if groups[label]:
            out.append(f"| [`{label}`](#{slug(label)}) | {len(groups[label])} |")
    out.append("")
    for label in LABELS:
        if not groups[label]:
            continue
        out += [f"## {label}", "", LABEL_TEXT[label][1 if zh else 0], ""]
        for name, url, section in groups[label]:
            where = PROJECT_SECTIONS[section] if zh else section
            out.append(f"- [{name}]({url}) · {where}")
        out.append("")
    return "\n".join(out)


def main():
    write = "--write" in sys.argv
    readme, readme_zh = ROOT / "README.md", ROOT / "README.zh-CN.md"
    projects = parse_projects(readme)
    datasets = count_datasets(readme)

    for svg, pattern in [("hero.svg", r"(\d+) projects · (\d+) datasets"),
                         ("hero.zh-CN.svg", r"(\d+) 个项目 · (\d+) 个数据集")]:
        text = (ROOT / "assets/readme" / svg).read_text()
        for m in re.finditer(pattern, text):
            if (int(m.group(1)), int(m.group(2))) != (len(projects), datasets):
                err(f"assets/readme/{svg}", 0,
                    f"says {m.group(1)} projects and {m.group(2)} datasets, README has "
                    f"{len(projects)} and {datasets}")

    en_urls = {url for _, url, _, _ in projects}
    for name, (start, lines) in sections(readme_zh.read_text()).items():
        for offset, line in enumerate(lines, 1):
            if line.startswith("| [") or line.startswith("- ["):
                url = LINK.search(line).group(2)
                if "news.ycombinator.com" not in url and url not in en_urls and name.startswith("「"):
                    err(readme_zh.name, start + offset, f"{url} is not in README.md")

    for path in [readme, readme_zh]:
        check_toc(path)

    for lang, path in [(False, ROOT / "docs/by-source.md"), (True, ROOT / "docs/by-source.zh-CN.md")]:
        want = by_source(projects, lang)
        if write:
            path.write_text(want)
        elif not path.exists() or path.read_text() != want:
            err(path.relative_to(ROOT), 0, "out of date: run python3 scripts/validate_list.py --write")

    for path in sorted(ROOT.glob("*.md")) + sorted(ROOT.glob("docs/*.md")) + sorted(ROOT.glob("data/*.md")):
        check_links(path)

    for e in errors:
        print(e)
    print(f"{len(projects)} projects, {datasets} datasets, {len(errors)} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
