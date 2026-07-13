# Customer Problems

## OP-001

### Problem
Teams can execute AI-assisted tickets correctly while still selecting unevidenced or low-value work.

### Who Has It
Product and engineering teams operating multiple agentic workstreams.

### Evidence
- The existing canonical trace begins at PRD intent.
- Feature requests can otherwise enter from conversation without an outcome gate.

### Frequency and Severity
Recurring and high impact because downstream correctness cannot repair an incorrect product bet.

### Current Workaround
Unstructured briefs, chat history, or disconnected product-management tools.

## OP-002

### Problem
Proofstack (the `niche-finder` product) only helps after a founder already has a niche hypothesis: creating an investigation requires a written segment/workflow summary, and Market, Segment, Hypothesis, and Evidence records must be added manually. There is no guided pre-hypothesis path that captures raw signals and sources, explores markets and recurring workflows, drills into candidate segments (roles, consequences, alternatives, accessibility), and compares candidates before one is promoted into a falsifiable investigation.

### Who Has It
Founders and product teams using Proofstack to discover which niche deserves investigation — observed directly in our own dogfood usage (2026-07-13 session), where the product could manage a supplied hypothesis but could not help discover one.

### Evidence
- Dogfood session (2026-07-13): the only executable path was create investigation → manually add Market/Segment/Hypothesis/Evidence records → validate, experiment, productize; every pre-hypothesis step happened outside the product.
- The product's worked example is a seeded synthetic demo hypothesis (the accounting example in `seed.ts`, with fictional evidence and founder-access claims), not a discovered or validated one — so no real discovery has ever run end to end (FINDING-001).
- The Proofstack product spec promises a source → observe → define path; the current build implements manage-and-validate but not the discovery funnel (founder dogfood report, tracked as dogfood issue #5).

### Frequency and Severity
Blocks the first step of every real usage session. High severity because the product's core promise is niche discovery, and validation quality cannot compensate for investigating the wrong — or a fabricated — hypothesis.

### Current Workaround
Do discovery in ad-hoc notes and chat, then hand-enter a summary and records — or, worse, reuse the seeded synthetic demo hypothesis as if it were real market input.
