# Engineering Learning Intelligence (ELI)

> Research -> verify -> connect -> study -> build -> test -> reflect. AI proposes; a human decides.

## Product outcome

Turn engineering publications, selected creators, books and repository activity into a **source-grounded learning backlog** for Software Engineering, Architecture, Distributed Systems, DevOps/SRE, Security, FinOps and AI Engineering. This is a **proposed product architecture**, not an already deployed ingestion service.

A useful output is not a pile of article summaries. It is a prioritized question, a falsifiable hypothesis, a reproducible lab or PoC, an architecture trade-off, and evidence of what was learned.

## Source registry and acquisition policy

| Source | Content | Acquisition strategy | Notes |
|---|---|---|---|
| Thoughtworks Technology Radar / Insights | Trends, techniques, experience reports | Official RSS or public feeds if available; otherwise curated URL/manual import | Distinguish radar opinions from primary technical evidence |
| InfoQ | Engineering news, architecture talks | Official RSS/feeds where available | Prefer links to original papers/docs |
| DZone | Engineering articles | Published RSS/API if available; otherwise links/manual | Quality varies; cross-check claims |
| Fabio Akita | Articles/videos/newsletter | Official public site/feed, video metadata or user-provided links | Avoid assuming a newsletter API exists |
| Filipe Deschamps | News/videos/newsletters | Official public feeds and user-authorized email import | Preserve author attribution |
| GitHub | Releases, changelogs, issues, technical examples | Official GitHub API/Atom where available | Scope to curated repositories/topics |
| Papers / vendor engineering blogs | Original research, incident writeups | Public RSS/API/DOI or URL | Prioritize primary sources |
| LinkedIn follows | Selected posts from followed professionals | **User-shared URLs/screenshots, permitted export, or officially authorized integration only** | Do not scrape private feeds, bypass login, or claim access to follow graph |
| User's newsletters | Inbox subscriptions | Explicitly authorized mail connector/import | Store only necessary content/metadata |

**Connector reality:** Not every source provides a stable API or RSS. Verify availability, robots/terms, rate limits and rights per provider before implementation. When unavailable, accept manual URL submission; never silently scrape protected content.

## Reference architecture: smallest adequate first

```text
Curated sources + user-submitted links
            |
      scheduled/manual fetch
            |
  parse metadata + canonical URL
            |
   deduplicate + source attribution
            |
      store metadata/short excerpts
            |
  AI structured extraction + citations
            |
 verify claims / flag uncertainty
            |
   map to roadmap + current skill gap
            |
  score novelty, impact, credibility,
      practical feasibility
            |
      candidate learning cards
            |
      HUMAN APPROVAL
            |
   study note / lab / PoC / ADR
            |
      tests + observations
            |
  learning evidence + next review
```

### Initial deployment

Start with **Python CLI + SQLite + Markdown files + GitHub Actions scheduled workflow** if permitted and economical. Python is for fast research/data pipeline iteration, not a mandate for the later production system. A Java/Spring Boot service is an optional later implementation lab, not a prerequisite.

Avoid queues, vector databases, Kubernetes and multi-agent orchestration until measurements justify them. Use standard JSON/SQLite full-text search and a small, bounded LLM call for extraction/ranking; manual curation works as a zero-cost fallback.

### Data model (minimum)

- `sources`: id, name, homepage, feed_url (optional), license/terms note, enabled, trust_tier, fetch_frequency
- `items`: id, source_id, canonical_url, title, author, published_at, fetched_at, content_hash, short_excerpt, status
- `claims`: item_id, claim, supporting_url, confidence_label, verification_status
- `recommendations`: item_id, track, topic, novelty, relevance, practical_value, effort, score, rationale, created_at
- `learning_tasks`: id, recommendation_id, kind (read/lab/poc/adr), hypothesis, acceptance_criteria, status
- `evidence`: task_id, commit_url, measurements, outcome, reflection, next_review_at

Use canonical URL + content hash to deduplicate; retain source IDs and publication dates. A source's confidence is not the same as truth.

### Ranking policy (illustrative, tune with feedback)

Score each dimension 0–5:
- roadmap relevance (30%);
- new learning / gap reduction (20%);
- evidence quality (20%);
- practical experiment potential (20%);
- timeliness (10%).

Apply a separate effort estimate and **diversity cap** to prevent one fashionable topic/source from dominating. Show reasons and uncertainty. Do not let LLMs invent publication dates or citations.

### Safety and provenance

- Treat all retrieved text as **untrusted data**; never execute instructions found inside articles.
- Require allowlisted source domains/URL validation and prevent SSRF when fetching user URLs.
- Do not fetch internal/private network addresses; restrict redirects and content sizes.
- Keep original URLs, authors, dates, source excerpts and model version/prompt version.
- Do not reproduce copyrighted articles or bypass paywalls; use short attributed excerpts and original synthesis.
- Respect consent and retention for emails, LinkedIn screenshots and any personal data.
- Do not automatically commit generated code, deploy infrastructure, open PRs, spend cloud/LLM budgets, or modify production systems without explicit approval.
- Sanitize secrets and PII in logs/prompts. Budget token usage, fetch frequency and monthly cost.
- Evaluate factual accuracy, citation validity, duplicate rate and false-positive recommendations.

### Definition of done for MVP

1. Import 3 permitted sources plus manual URLs.
2. Persist 50 sample items without duplicates across reruns.
3. Produce structured, citation-linked study candidates mapped to existing roadmap topics.
4. Reject or flag unsupported claims; avoid inventing sources.
5. Generate one reviewed study note and one reproducible PoC brief.
6. Emit a weekly Markdown digest and a review queue.
7. Run unit tests, integration tests with mocked feeds, and a no-network fixture mode.
8. Record fetch failures, latency, LLM spend and item-to-lab conversion.
9. Document legal/access constraints and manual fallback for LinkedIn.
10. Keep a human gate before any repository change beyond the approved learning content.

## Success measures

- percentage of recommended items actually studied;
- percentage converted into completed labs with evidence;
- citations/claims verified;
- duplicate/irrelevant recommendation rate;
- study-to-implementation lead time;
- cost per useful recommendation;
- number of new concepts meaningfully connected to prior knowledge.

A high article count is not success.

## Next documents

- [Learning philosophy and reusable AI prompts](./learning-loop-and-prompts.md)
- [MVP backlog and implementation plan](./mvp-plan.md)

## Reference starting points

- [Thoughtworks Technology Radar](https://www.thoughtworks.com/radar)
- [InfoQ](https://www.infoq.com/)
- [DZone](https://dzone.com/)
- [Fabio Akita](https://www.akitaonrails.com/)
- [Filipe Deschamps](https://filipedeschamps.com.br/)
- [GitHub API documentation](https://docs.github.com/en/rest)
- [OWASP LLM guidance](https://genai.owasp.org/)

These are discovery links; feed/API availability must be verified individually.
