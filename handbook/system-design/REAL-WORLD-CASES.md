# Real-World Architecture Case Studies — Source Catalog

This catalog records topics **visible in a user-supplied screenshot** of a Neo Kim / System Design One LinkedIn post and direct newsletter links shared by the user. It does not claim to verify the article content or the companies' private production implementations. Treat descriptions as third-party educational material until independently corroborated.

## Directly supplied newsletter reading links

| Case | Reading | Design focus to investigate (our questions, not verified article claims) |
|---|---|---|
| Apache Kafka | [How Kafka Works](https://newsletter.systemdesign.one/p/how-kafka-works) | Partitioning, consumer groups, log retention, durability, replication, ordering |
| YouTube | [YouTube System Design](https://newsletter.systemdesign.one/p/youtube-system-design) | Upload, transcoding, object storage, CDN, metadata, recommendations |
| Google Docs | [How Does Google Docs Work](https://newsletter.systemdesign.one/p/how-does-google-docs-work) | Collaborative editing, OT/CRDT trade-offs, conflict resolution, offline sync |
| WhatsApp | [WhatsApp System Design](https://newsletter.systemdesign.one/p/whatsapp-system-design) | Message delivery, ordering, offline clients, fanout, privacy |
| Airbnb | [Airbnb System Design](https://newsletter.systemdesign.one/p/airbnb-system-design) | Search, availability, booking races, inventory consistency |

## Additional topics visible in the shared screenshot

The screenshot also lists: **Google Search**, **Spotify**, **Slack**, **Reddit**, **Bluesky**, **Twitter/X**, and **Uber ETA computation**. These are confirmed *topics on the screenshot*, not verified article contents or direct canonical URLs. The post claims 15 studies; only 12 topic names are visible in the supplied image, so we intentionally do not invent the remaining three.

## Additional user-mentioned topic candidates

**Amazon Prime Video** and other large-company architecture examples are requested areas of interest, but no individual article URL was supplied for them. Add direct links only after verification.

## Recommended study order

1. **Kafka:** durable event logs, partitioning, ordering; connect to our webhook/event-ingestion lab.
2. **WhatsApp:** messaging delivery semantics and recovery; connect to the notification service and chat labs.
3. **Google Docs:** concurrent collaboration; compare OT and CRDT with a small two-client prototype.
4. **YouTube:** media ingestion and asynchronous processing; prototype a local pipeline with simulated transcoding.
5. **Airbnb:** transaction isolation and inventory; reproduce double-booking races and verify the fix.
6. **Uber ETA:** model a routing/ETA service with explicitly synthetic traffic data and measured performance.
7. **Search, social feeds and streaming:** compare indexing, fanout, ranking, recommendation and cost choices.

A marketing promise such as "god-level in 3 weeks" is not an engineering outcome or guaranteed timeline. Depth, experiments and measured trade-offs determine progress.

## Repeatable case-study review

For each source:

- **Source audit:** author, publication date, direct URL, official documentation cross-check, confidence levels.
- **Architecture reconstruction:** actors, requirements, data flows, components, consistency boundaries and failure modes.
- **Challenge:** which assumptions are speculative? Which choices are historical or context-dependent?
- **Lab extraction:** one bounded architectural question and minimal PoC.
- **Evidence:** reproducible tests, latency/throughput/cost measurements, ADR, what would change the decision.

Use [CASE-TEMPLATE.md](CASE-TEMPLATE.md) to capture the actual design exercise. Do not copy newsletter article bodies into the repository; link and paraphrase with attribution.
