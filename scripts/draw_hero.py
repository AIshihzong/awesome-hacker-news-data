"""Draw assets/readme/hero.svg and hero.zh-CN.svg.

    python3 scripts/draw_hero.py assets/readme

Update the project and dataset counts in TEXT when scripts/validate_list.py asks for it.
"""
import sys
from pathlib import Path

out = Path(sys.argv[1])
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans CJK SC', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
COLORS = {"open-index": "#3fb950", "Algolia API": "#58a6ff", "HackerTube data": "#bc8cff", "not stated": "#d29922"}

TEXT = {
    "en": dict(
        title="Awesome Hacker News Data: every HackerTube for X, the datasets behind them, and the gotchas in the data",
        desc="Unofficial list of 76 projects and 9 datasets. Example rows: HackerTube, 6,454 YouTube videos, source open-index; HackerBooks, about 16.5k books, source not stated; HackerPods, podcasts, source Algolia API; HackTok, a vertical video feed, source HackerTube data.",
        kicker="AWESOME LIST · HACKER NEWS DATA",
        lines=["Every “HackerTube for X”,", "the data behind each one,", "and the traps in that data."],
        footer="76 projects · 9 datasets · source on every entry",
        head="SITE · WHAT IT RANKS", tag="DATA",
        rows=[("HackerTube", "6,454 YouTube videos", "open-index"),
              ("HackerBooks", "~16.5k books", "not stated"),
              ("HackerPods", "Podcasts and episodes", "Algolia API"),
              ("HackTok", "HackerTube as a vertical feed", "HackerTube data")],
    ),
    "zh-CN": dict(
        title="Awesome Hacker News Data：所有「HackerTube for X」、它们背后的数据，以及数据里的坑",
        desc="非官方合集，收录 76 个项目和 9 个数据集。示例：HackerTube，6,454 个 YouTube 视频，数据来源 open-index；HackerBooks，约 1.65 万本书，来源未说明；HackerPods，播客，来源 Algolia API；HackTok，竖屏视频流，来源 HackerTube 导出数据。",
        kicker="AWESOME LIST · HACKER NEWS 数据",
        lines=["所有「HackerTube for X」，", "每个用的是哪份数据，", "以及数据里的坑。"],
        footer="76 个项目 · 9 个数据集 · 每条标注数据来源",
        head="网站 · 排的是什么", tag="数据",
        rows=[("HackerTube", "6,454 个 YouTube 视频", "open-index"),
              ("HackerBooks", "约 1.65 万本书", "not stated"),
              ("HackerPods", "播客和单集", "Algolia API"),
              ("HackTok", "竖屏刷 HackerTube", "HackerTube data")],
    ),
}


def svg(t):
    p = []
    a = p.append
    a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" width="1200" height="420" role="img" aria-labelledby="t d">')
    a(f'<title id="t">{t["title"]}</title>')
    a(f'<desc id="d">{t["desc"]}</desc>')
    a('<defs>')
    a('<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#2a2420"/></pattern>')
    a('<linearGradient id="glow" x1="0" y1="0" x2="1" y2="0.4"><stop offset="0" stop-color="#ff6600" stop-opacity="0.16"/><stop offset="1" stop-color="#ff6600" stop-opacity="0"/></linearGradient>')
    a('</defs>')
    a('<rect width="1200" height="420" rx="20" fill="#16120f"/>')
    a('<rect width="1200" height="420" rx="20" fill="url(#dots)"/>')
    a('<rect width="1200" height="420" rx="20" fill="url(#glow)"/>')
    a(f'<text x="56" y="76" font-family="{MONO}" font-size="18" letter-spacing="2" fill="#a39385">{t["kicker"]}</text>')
    a(f'<rect x="56" y="104" width="64" height="64" rx="6" fill="#ff6600"/>')
    a('<path d="M88 120 L108 152 L68 152 Z" fill="#ffffff"/>')
    a(f'<text x="138" y="140" font-family="{SANS}" font-size="34" font-weight="800" fill="#f6f0ea">Awesome</text>')
    a(f'<text x="138" y="172" font-family="{SANS}" font-size="30" font-weight="700" fill="#ff8a3d">Hacker News Data</text>')
    for i, line in enumerate(t["lines"]):
        a(f'<text x="56" y="{236 + i * 38}" font-family="{SANS}" font-size="27" fill="#ddd2c8">{line}</text>')
    a('<line x1="56" y1="346" x2="560" y2="346" stroke="#3a302a" stroke-width="2"/>')
    a(f'<text x="56" y="384" font-family="{MONO}" font-size="18" fill="#a39385">{t["footer"]}</text>')
    a('<rect x="612" y="36" width="536" height="348" rx="16" fill="#1f1915" stroke="#3a302a" stroke-width="2"/>')
    a(f'<text x="640" y="78" font-family="{MONO}" font-size="18" letter-spacing="1" fill="#a39385">{t["head"]}</text>')
    a(f'<text x="1120" y="78" font-family="{MONO}" font-size="18" letter-spacing="1" fill="#a39385" text-anchor="end">{t["tag"]}</text>')
    for i, (name, what, src) in enumerate(t["rows"]):
        top = 96 + i * 72
        c = COLORS[src]
        w = len(src) * 10.8 + 28
        a(f'<line x1="640" y1="{top}" x2="1120" y2="{top}" stroke="#3a302a" stroke-width="2"/>')
        a(f'<text x="640" y="{top + 33}" font-family="{SANS}" font-size="22" font-weight="600" fill="#f6f0ea">{name}</text>')
        a(f'<text x="640" y="{top + 60}" font-family="{SANS}" font-size="18" fill="#a39385">{what}</text>')
        a(f'<rect x="{1120 - w:.1f}" y="{top + 20}" width="{w:.1f}" height="34" rx="17" fill="{c}" fill-opacity="0.16" stroke="{c}" stroke-width="1.5"/>')
        a(f'<text x="{1120 - w / 2:.1f}" y="{top + 42}" font-family="{MONO}" font-size="18" font-weight="700" fill="{c}" text-anchor="middle">{src}</text>')
    a('</svg>')
    return "\n".join(p) + "\n"


out.mkdir(parents=True, exist_ok=True)
(out / "hero.svg").write_text(svg(TEXT["en"]))
(out / "hero.zh-CN.svg").write_text(svg(TEXT["zh-CN"]))
