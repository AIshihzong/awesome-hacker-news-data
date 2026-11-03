# Contributing

Pull requests are welcome. To add a project:

1. **Put it in the right section**: the "HackerTube for X" table, apps and ports, search and
   exploration, infrastructure, or analysis.
2. **Write one line** on what it does. Use concrete numbers where you have them
   ("ranks 9,434 blogs from 10.7M links", not "a great tool for blogs").
3. **Label the data source** with `open-index`, `HackerTube data`, `Algolia API`, `HN API`,
   `BigQuery` or `not stated`. Link the README line, site page or author post that backs the label
   in your PR description. If you can't find one, use `not stated`.
4. **Check the link works** and the project is public. A weekly link check flags dead links, and projects
   that stay dead for a month are removed.

Fixing a wrong label or a number is as valuable as adding a project.

Changes to `queries/` should run against `00_setup.sql` on at least one month of data. Say which
month you tested in the PR.
