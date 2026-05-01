# Blinded Articles

Save anonymized article copies here for evaluator subagents.

Recommended path:

`comparing/blinded_articles/<run_id>/<article_id>.md`

Example:

`comparing/blinded_articles/run-2026-05-01-D001/Article_A.md`

Blinding requirements:

- Remove condition IDs, skill names, model names, and generation timestamps.
- Keep the article text unchanged.
- Assign article IDs randomly.
- Record the private map from article ID to source file in
  `../evaluation_log.md`.
- Do not show the private map to evaluator subagents.

