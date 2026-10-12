# Foundational AI Agent Papers — Research-to-Practice Reading Path

Source of discovery: user-shared LinkedIn screenshot (October 2026). The post lists nine fully visible papers and a partially visible tenth, *A Survey on Large Language Model Based Autonomous Agents*. This is a curated **study queue**, not evidence that the papers' claims generalize to modern production models.

## Reading order and primary references

| Phase | Paper | Primary reference | Engineering question |
|---|---|---|---|
| Reasoning | Chain-of-Thought Prompting Elicits Reasoning in Large Language Models | https://arxiv.org/abs/2201.11903 | When do examples of intermediate reasoning improve task success, and at what token cost? |
| Reasoning/action | ReAct: Synergizing Reasoning and Acting in Language Models | https://arxiv.org/abs/2210.03629 | When does tool-backed observation beat a single model answer? |
| Tool use | Toolformer: Language Models Can Teach Themselves to Use Tools | https://arxiv.org/abs/2302.04761 | How should a system decide whether a tool call is warranted? |
| Memory | Generative Agents: Interactive Simulacra of Human Behavior | https://arxiv.org/abs/2304.03442 | What is gained/lost by storing and retrieving agent memories? |
| Reflection | Reflexion: Language Agents with Verbal Reinforcement Learning | https://arxiv.org/abs/2303.11366 | Can feedback improve retries without updating model weights? |
| Search | Tree of Thoughts: Deliberate Problem Solving with Large Language Models | https://arxiv.org/abs/2305.10601 | When is branching search worth added calls and latency? |
| Orchestration | HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face | https://arxiv.org/abs/2303.17580 | When is model/tool orchestration better than a direct task-specific path? |
| Skills | Voyager: An Open-Ended Embodied Agent with Large Language Models | https://arxiv.org/abs/2305.16291 | When do reusable skills and feedback improve long-running tasks? |
| Multi-agent | AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation | https://arxiv.org/abs/2308.08155 | Does collaboration outperform a single well-designed agent under the same budget? |
| Survey | A Survey on Large Language Model based Autonomous Agents | https://arxiv.org/abs/2308.11432 | What components and evaluation dimensions recur across agent designs? |

Links are primary paper identifiers for the named works. Review versions, updates and later evaluations before treating findings as current best practice.

## Study method (apply to every paper)

1. State the actual problem and experimental assumptions.
2. Separate claims in the paper from results independently reproduced.
3. Compare with the **simplest adequate baseline** (deterministic code, retrieval + one model call, or one bounded tool loop).
4. Define measurable success, accuracy, latency, token spend, security and human effort.
5. Build the smallest reproducible PoC with fixtures and tests.
6. Inject tool failure, misleading retrieved content, prompt injection, timeout and duplicate actions where relevant.
7. Record observations, alternatives, limitations and an ADR; do not award mastery for merely summarizing or generating code.

## Engineering Learning Intelligence (ELI) application

**Lab A — ReAct vs deterministic pipeline:** Take ten curated engineering articles. Baseline: feed ingestion + deterministic topic mapping. Candidate: bounded LLM/tool loop that requests primary sources for unsupported claims. Compare citation accuracy, relevant recommendations, runtime and cost. Restrict network tools and require human review.

**Lab B — Reflexion:** Given an evaluation fixture of failed study-card drafts, compare one-shot output, a deterministic validation-and-retry loop and a bounded self-critique loop. Measure improvement on held-out cases and extra tokens. No automatic repository writes.

**Lab C — Tree of Thoughts:** For an architecture trade-off (Postgres outbox vs managed queue vs Kafka), compare a single structured evaluation against branching alternative generation plus a fixed rubric. Verify that extra reasoning improves decision quality, not merely length.

**Lab D — Memory:** Compare no memory, curated user-approved learning history, and retrieval from prior study cards. Measure recommendation relevance and stale-memory failures; avoid storing sensitive personal data unnecessarily.

**Lab E — Single vs multi-agent:** Compare one bounded researcher against researcher+critic+lab-designer agents using identical sources, test fixtures and a strict cost ceiling. Use multiple agents only if improvement is reproducible.

## Evaluation scorecard

- Citation correctness and source provenance
- Factual accuracy / unsupported claims
- Task completion and practical usefulness
- Tool-call correctness and permission compliance
- Resistance to prompt injection and untrusted-source instructions
- Reproducibility and recovery after failure
- Latency, token cost and total operating cost
- Human approval and auditability

## Integration rules

- ELI V1 stays a deterministic Python CLI + SQLite + permitted RSS/manual URLs.
- These papers inform **future optional AI experiments**, not mandatory V1 dependencies.
- No autonomous browsing of private LinkedIn feeds, scraping behind authentication, secret exposure, or unapproved writes/deployments.
- Do not confuse Chain-of-Thought research with a requirement to expose hidden model reasoning; evaluate observable outputs and intermediate tool actions instead.
- Keep original sources linked and produce original summaries rather than copying full papers.

## Related roadmap

- [AI learning intelligence architecture](../learning-intelligence/README.md)
- [Reusable AI study prompts](../learning-intelligence/learning-loop-and-prompts.md)
- [ELI MVP implementation plan](../learning-intelligence/mvp-plan.md)
