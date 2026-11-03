# Build a slim local DuckDB copy of open-index/hacker-news (no comment text, about 1.1 GB), one month per step.
# Resumable: rerun after an interruption and it skips months already loaded.
# Usage: python build_local_db.py hn.duckdb
import sys, csv, io, urllib.request, duckdb

db = sys.argv[1]
BASE = "https://huggingface.co/datasets/open-index/hacker-news/resolve/main"
stats = list(csv.DictReader(io.StringIO(urllib.request.urlopen(f"{BASE}/stats.csv").read().decode())))
c = duckdb.connect(db)
c.sql("INSTALL httpfs; LOAD httpfs; SET threads=8; SET enable_progress_bar=false; SET TimeZone='UTC';")
c.sql("""CREATE TABLE IF NOT EXISTS stories (id UINTEGER, type TINYINT, "by" VARCHAR, time TIMESTAMPTZ, dead UTINYINT,
         deleted UTINYINT, score INTEGER, descendants INTEGER, title VARCHAR, url VARCHAR, text_len INTEGER, nkids INTEGER)""")
c.sql("""CREATE TABLE IF NOT EXISTS comments (id UINTEGER, "by" VARCHAR, time TIMESTAMPTZ, parent UINTEGER, dead UTINYINT,
         deleted UTINYINT, text_len INTEGER)""")
c.sql("CREATE TABLE IF NOT EXISTS done (f VARCHAR)")
done = {r[0] for r in c.sql("SELECT f FROM done").fetchall()}
for i, s in enumerate(stats):
    f = f"data/{s['year']}/{s['year']}-{int(s['month']):02d}.parquet"
    if f in done: continue
    src = f"read_parquet('{BASE}/{f}')"
    c.sql(f"""INSERT INTO stories SELECT id, type, "by", time, dead, deleted, score, descendants, title, url,
              length(text), len(kids) FROM {src} WHERE type <> 2""")
    c.sql(f"""INSERT INTO comments SELECT id, "by", time, parent, dead, deleted, length(text) FROM {src} WHERE type = 2""")
    c.sql(f"INSERT INTO done VALUES ('{f}')")
    print(i + 1, "/", len(stats), f, flush=True)
print("DONE", c.sql("SELECT (SELECT count(*) FROM stories), (SELECT count(*) FROM comments)").fetchall())
