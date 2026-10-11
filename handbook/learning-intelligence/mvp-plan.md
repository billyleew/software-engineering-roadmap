# Engineering Learning Intelligence — MVP Implementation Plan

## Scope and boundaries

Deliver a reproducible research-to-study pipeline in the existing roadmap repository. Do not introduce production hosting, scraping of protected feeds, browser automation or paid infrastructure in v0.

### Proposed structure

```text
learning-intelligence/
  pyproject.toml
  README.md
  src/eli/
    cli.py
    config.py
    models.py
    feeds.py
    manual_import.py
    normalize.py
    storage.py
    rank.py
    llm.py
    render.py
  config/
    sources.example.yaml
    roadmap-topics.yaml
  tests/
    fixtures/
    test_normalize.py
    test_deduplicate.py
    test_rank.py
    test_render.py
    test_pipeline_integration.py
  output/            # generated locally; decide what to commit
```

Keep code separate from `handbook/` so the handbook remains useful without running software.

## Vertical slices

### Slice 0 — Source/access feasibility
- Confirm official feeds/API access for Thoughtworks, InfoQ, DZone and chosen creator sources.
- Document robots/terms/licensing, rate limits and fallback.
- LinkedIn: manual link/screenshot or officially permitted access only.
- Decide what metadata/excerpts can be stored.

**Acceptance:** a source registry with verified access method and no protected scraping assumptions.

### Slice 1 — Deterministic ingestion (no AI)
- Define typed `Source` and `Item` contracts.
- Fetch permitted RSS/Atom feeds with timeout, size limits and safe URL validation.
- Manual `add-url` path for LinkedIn and creator posts; no login scraping.
- Normalize URL/date/title; hash and deduplicate; SQLite storage.
- Implement `eli fetch`, `eli import-url`, `eli list`.
- Fixtures for offline tests; handle invalid feeds, 429, 500, redirects and duplicates.

**Acceptance:** idempotent rerun on fixtures; failures logged without losing good items.

### Slice 2 — Roadmap relevance
- Create topic taxonomy from existing six-track roadmap.
- Deterministic keyword/topic baseline before LLM ranking.
- Store explanation for each relevance decision.
- Human feedback: relevant / not relevant / already known.

**Acceptance:** testable ranking and auditable decisions.

### Slice 3 — AI synthesis behind a port
- `ResearchModel` interface with mock and optional real LLM adapter.
- JSON-schema-validated outputs; strict URL provenance.
- Never send secrets/private newsletters without authorization.
- Bound input length, token cost and retries.
- Treat retrieved content as data; do not follow embedded instructions.
- Fail closed to manual review when evidence is missing.

**Acceptance:** golden-fixture tests for citations, unsupported claims and prompt injection attempts.

### Slice 4 — Study/PoC generation
- Render a Markdown study card using the approved prompt contract.
- Generate PoC briefs with baseline, alternatives, hypothesis, tests, failure injection, telemetry, costs and ADR template.
- Require human approval before committing generated outputs or creating issues/PRs.

**Acceptance:** one reproducible study card and one experiment proposal from fixtures.

### Slice 5 — Weekly digest and feedback
- CLI `eli digest --since 7d` generates concise Markdown with ranked candidates.
- Include source links, why relevant, recommended action and estimated effort.
- Record chosen/ignored/completed items; calculate useful recommendation rate.
- Optionally schedule GitHub Actions after verifying permissions, cost and secrets.

**Acceptance:** rerunnable digest with no duplicate recommendations and explicit dates.

## Quality gates

### Unit tests
- URL normalization and deduplication
- topic mapping/scoring
- schema validation
- Markdown rendering
- prompt-injection data handling

### Integration tests
- fixture feed -> SQLite -> rank -> Markdown
- HTTP error, timeout, malformed feed, rate limit
- LLM mock -> structured candidate
- interrupted/repeated run -> idempotency

### Security tests
- localhost/private-IP/metadata endpoint SSRF rejection
- redirect restrictions
- oversized payload rejection
- HTML sanitization
- secrets/PII excluded from logs
- prompt injection does not trigger tools/actions

### Observability
- items fetched/accepted/skipped;
- duplicate ratio;
- fetch errors and latency;
- LLM cost/tokens and invalid-output ratio;
- recommendation acceptance;
- completed labs per month.

## First concrete example

Source: InfoQ article about a new queue or distributed data pattern.

1. Extract claim and cite article + primary docs.
2. Compare to `handbook/software-architecture/distributed-systems.md`.
3. Create a candidate lab: PostgreSQL outbox vs managed queue.
4. Implement a small service with metrics, retries and idempotency.
5. Inject consumer failure and duplicate delivery.
6. Compare throughput, end-to-end latency, recovery, operational cost.
7. Document evidence and ADR; update handbook only if conclusions are supported.

## Exit criteria before next architecture step

- A working local pipeline with fixtures and tests.
- At least one real permitted source integrated.
- One reviewed study card + one completed lab with evidence.
- Measured pipeline cost and reliability.
- No need for Redis/Kafka/Kubernetes/vector DB unless a real constraint appears.

## Future options (not MVP requirements)

- GitHub Issues for accepted learning tasks.
- Semantic search/vector retrieval only if keyword search fails at scale.
- Email connector for user-authorized newsletters.
- Browser/manual capture for inaccessible sources with rights respected.
- Web UI, notifications and multiple user profiles.
- AI agents for deeper research with strict tool permissions and approvals.
