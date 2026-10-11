# Engineering Learning Intelligence — Version 1

Local research inbox: manually save public URLs and ingest **metadata only** from RSS/Atom feeds that the publisher permits. No LLM, scraping, LinkedIn account access, paid hosting, background scheduler or auto-generated repository changes yet.

## Requirements

Python 3.11+.

```bash
cd learning-intelligence
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
pytest -q
```

From repository root, for example:

```bash
eli --db learning-intelligence/data/eli.sqlite3 add-url \
  'https://www.thoughtworks.com/radar' \
  --title 'Thoughtworks Technology Radar' --source Thoughtworks

eli --db learning-intelligence/data/eli.sqlite3 list
```

To ingest an **officially published, permitted RSS/Atom URL** (verify the current feed URL and terms first):

```bash
eli --db learning-intelligence/data/eli.sqlite3 fetch 'https://PUBLISHER/VERIFIED-FEED' --source Publisher
```

The CLI intentionally does not assume that Thoughtworks, InfoQ, DZone, creator newsletters or LinkedIn provide unrestricted public feeds. Use `add-url` for manually selected LinkedIn posts; it stores title/link only and does not log in or fetch their content.

## Commands

- `add-url URL --title TITLE --source SOURCE`: store manual reference; no network call.
- `fetch FEED_URL --source SOURCE`: validate public URL, fetch RSS/Atom metadata and deduplicate.
- `list [--limit N]`: print JSON entries.

`--db PATH` can be supplied before the command, or use `ELI_DB`. Database is created on demand. Re-imports do not duplicate canonical URLs.

## Current limitations and threat model

The fetcher rejects private/loopback/reserved DNS results, refuses redirects, enforces a response size limit and timeout. DNS rebinding remains possible between resolution and connection: **do not expose it as a public URL-fetching service** without network-level egress controls or a hardened proxy. Feed item links are stored as references and not fetched. Feed publishers' terms/robots/licensing must be checked before use.

Do not import private newsletters or personal data without explicit permission. Do not commit the local SQLite database. Content is metadata only; no article-body archiving or redistribution.

## Architecture

```text
manual URL / permitted RSS feed
  -> URL normalization
  -> SQLite UNIQUE canonical_url
  -> JSON CLI listing
```

Tests use an in-memory feed fixture and temporary SQLite databases, so they do not need external network access.

## Next slice

Verify publisher feeds, add a curated source registry and topic relevance scoring, then introduce an optional source-grounded LLM adapter with evaluation fixtures and explicit human approval. See [MVP plan](../handbook/learning-intelligence/mvp-plan.md).
