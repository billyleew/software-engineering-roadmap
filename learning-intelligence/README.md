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

## First useful learning digest

After importing a few source links, generate a prioritized Markdown review queue:

```bash
eli digest --limit 10
eli digest --limit 10 --output output/weekly-review.md
```

This first classifier is **deterministic** and matches title keywords against seven roadmap tracks; it explains topic matches and flags unmatched titles for manual triage. It is intentionally not an AI model and does not verify article claims. Review original sources before deciding to study or build a PoC. No scheduling or background access is enabled yet.

**First study habit:** Spend 20 minutes on discovery (5 minutes finding one item, 10 minutes understanding it, 5 minutes questioning assumptions). Reserve a separate lab session to implement, break, measure and document the idea.

## Version 1.1 — Curated multi-source ingestion

From `learning-intelligence/` after `pip install -e '.[test]'`:

```bash
eli sources
eli fetch-all
eli list --limit 20
eli digest --limit 10 --output output/weekly-review.md
python -m pytest -q
```

The checked-in `config/sources.example.json` is **opt-in**: publisher RSS endpoints are *unverified candidates*, so `enabled` and `access_reviewed` are initially false. Thus `eli fetch-all` initially reports skipped sources, not newly imported articles. This is expected.

To activate a source, first confirm its current official RSS/Atom URL, access terms and rate limits. Copy the example to `config/sources.local.json`, update the URL, set `access_reviewed: true` and `enabled: true`, then:

```bash
eli sources --sources config/sources.local.json
eli fetch-all --sources config/sources.local.json
```

Keep local registry modifications out of version control if they contain personal information. `fetch-all` continues past a failing feed, reports per-source results, deduplicates across feeds and introduces a short delay between enabled sources. It does not scrape articles or LinkedIn. The metadata classifier still needs human review; no LLM is called.

**Security limitation:** DNS checks occur before the HTTP connection, so this is a local trusted-user tool, not a hardened publicly exposed fetch service. Do not use it for arbitrary URLs from untrusted users without network egress enforcement.

### V1.1 validation checklist

- `python -m pytest -q` passes, including partial-failure and repeat-ingestion tests.
- `eli sources` lists registry entries with expected opt-in states.
- `eli fetch-all` with default registry safely skips unreviewed sources.
- A reviewed, permitted live feed imports real metadata; rerun yields duplicates, not new rows.
- `eli digest` includes newly ingested topics.

Live feed availability and GitHub Actions results must be verified independently; the code commit alone does not prove successful external ingestion.
