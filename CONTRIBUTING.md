# Contributing

The easiest way to suggest a project is the
[project form](https://github.com/AIshihzong/awesome-hacker-news-data/issues/new?template=project.yml).
Pull requests are welcome too. If a coding agent is writing the change, point it at
[AGENTS.md](AGENTS.md).

To add a project:

1. **Put it in the right section**: the "HackerTube for X" table, apps and ports, search and
   exploration, infrastructure, or analysis.
2. **Write one line** on what it does. Use concrete numbers where you have them
   ("ranks 9,434 blogs from 10.7M links", not "a great tool for blogs").
3. **Label the data source** with `open-index`, `HackerTube data`, `HackerBooks data`, `OpenPipe`,
   `Algolia API`, `HN API`, `BigQuery`, `own data` or `not stated`. Link the README line, site
   page or author post that backs the label in your PR description. If you can't find one, use
   `not stated`.
4. **Run the validator**: `python3 scripts/validate_list.py --write`. It regenerates
   [docs/by-source.md](docs/by-source.md) and checks labels, links and counts. Commit what it
   writes, and update the counts in `assets/readme/hero*.svg` if it asks you to.
5. **Check the link works** and the project is public. A weekly link check flags dead links, and
   projects that stay dead for a month are removed.

Fixing a wrong label or a number is as valuable as adding a project.

Changes to `queries/` should run against `00_setup.sql` on at least one month of data. Say which
month you tested in the PR.
