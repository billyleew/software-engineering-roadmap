# Case Study 02 — Video Platform

## What this case teaches

Large objects and asynchronous processing change architecture more than ordinary CRUD does.

Core topics:
- direct-to-object-storage uploads;
- metadata vs binary data;
- transcoding pipelines;
- asynchronous job processing;
- CDN delivery;
- cacheability;
- failure/retry semantics;
- cost as an architecture driver.

## Pass 1 — Small product

Assume:
- 4 engineers;
- 10k users;
- 500 uploads/day;
- average source video 300 MB;
- one region;
- basic playback on web/mobile.

### Functional requirements
- upload video;
- process/transcode;
- generate thumbnail;
- publish/unpublish;
- stream video;
- query processing state.

### Initial architecture

Do not proxy 300 MB files through the application unless there is a strong reason.

```text
Client
  |
  +--> API: request upload
  |       |
  |       +--> PostgreSQL metadata
  |       +--> signed upload URL
  |
  +----------------------> Object Storage
                              |
                              v
                         Processing Queue
                              |
                              v
                         Transcode Worker
                              |
                              +--> renditions
                              +--> thumbnails
                              v
                         Object Storage
                              |
                              v
                             CDN
                              |
                              v
                            Viewer
```

## Why metadata and media separate

Store metadata such as title, owner, visibility and processing state in a transactional database.

Store large binary media in object storage designed for durable blobs.

Do not put videos into relational database rows because "the database is already there".

## Processing state

```text
UPLOADING
 -> UPLOADED
 -> PROCESSING
 -> READY
 -> FAILED
```

Processing jobs must tolerate worker crashes and duplicate delivery.

Transcoding the same rendition twice may be acceptable if outputs are deterministic and writes are idempotent, but publishing state must remain controlled.

## Upload flow

1. Client requests an upload session.
2. API validates user/quota and creates metadata record.
3. API issues a short-lived scoped upload URL.
4. Client uploads directly to object storage.
5. Completion event/callback triggers processing.
6. Worker transcodes and updates state.

Consider multipart/resumable uploads for large files when real client/network behavior requires them.

## Streaming

Initially use standard HTTP-based adaptive streaming formats supported by chosen platform/tools.

The architecture question is not "build a video protocol" but:
- which renditions are needed;
- how chunks/manifests are stored;
- how content is cached at the edge;
- how access control works for private media.

## Observability baseline

Business:
- uploads started/completed;
- processing success rate;
- time from upload completion to READY;
- playback starts;
- playback failure rate.

Technical:
- upload error rate;
- processing queue depth/oldest age;
- worker duration/failures;
- storage errors;
- CDN hit ratio;
- origin bandwidth;
- egress cost;
- playback startup latency.

## Cost model

Video systems are strongly shaped by:
- storage;
- transcoding compute;
- network egress;
- CDN;
- number of generated renditions.

Generating every possible resolution/codec for every uploaded video may waste more money than it saves.

## Pass 2 — Growth pressure

Evidence:
- 50k uploads/day;
- processing delay > 45 minutes at peaks;
- many short videos;
- CDN hit ratio good, but egress cost rises materially.

Investigate separately:
- queue backlog;
- worker concurrency;
- transcoding CPU/GPU efficiency;
- rendition policy;
- storage lifecycle;
- geographic viewer distribution.

Possible changes:
- autoscale worker pool from queue age;
- prioritize shorter/newly published jobs;
- separate thumbnail and heavy transcode workloads;
- reduce unused renditions based on playback data;
- tune CDN cache policy.

Do not immediately split metadata API into ten microservices because transcoding is slow.

## Pass 3 — Global product

New requirements:
- creators in multiple regions;
- viewers globally;
- millions of plays/day;
- copyright/moderation workflows;
- private and public videos;
- processing tiers/priorities.

Potential evolution:
- regional upload ingress;
- replicated/distributed metadata read path where required;
- global CDN;
- event-driven processing pipeline;
- independent media-processing service/teams;
- asynchronous moderation/indexing workflows.

## Failure analysis

What if:
- upload succeeds but completion event is lost?
- queue delivers processing job twice?
- one rendition fails but others succeed?
- CDN cannot reach origin?
- object metadata says READY but manifest is missing?
- signed URL leaks?
- transcoder creates malformed output?

## ADR exercises

Write ADRs for:
1. direct-to-object-storage upload;
2. asynchronous transcoding;
3. object storage instead of DB blobs;
4. CDN adoption and success metric;
5. worker autoscaling based on queue age rather than only CPU;
6. rendition-generation policy based on actual usage.

## What not to add without evidence

Do not automatically add:
- Kafka instead of a simpler managed queue;
- multi-region active-active databases;
- custom CDN;
- separate service per processing step;
- Redis in front of every metadata query.

Let media volume, latency, cost and team boundaries determine evolution.