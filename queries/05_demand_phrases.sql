-- Product-demand signals: comments that say "I'd pay", "I wish there was", "is there a tool".
-- Expect roughly 1 in 5 matches to be a real product need; classify the rest away with an LLM.
SELECT id, "by", time,
       plain(text) AS text
FROM comments
WHERE dead = 0
  AND regexp_matches(lower(text),
      '\b(i''?d|i would|would happily) pay\b|take my money|\bi wish (there was|there were|someone would|someone made)\b|\bis there (a|an|any) (tool|app|service|product|saas)\b')
ORDER BY time DESC
LIMIT 500;
