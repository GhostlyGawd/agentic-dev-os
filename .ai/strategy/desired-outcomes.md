# Desired Outcomes

## O-001

### Outcome Statement
Teams using the operating system can trace every active delivery requirement to an evidenced customer problem and measurable product outcome.

### Metric
Product-chain coverage.

### Baseline
0% of PRDs linked above the product brief layer.

### Target
100% of active PRDs link to a validated bet, opportunity, and outcome.

### Time Horizon
At completion of M-002.

### Guardrail Metrics
Artifact validation time remains below two seconds locally and no duplicate canonical source is introduced.

## O-002

### Outcome Statement
A founder using Proofstack (the `niche-finder` product) can start from raw market signals and reach one falsifiable investigation whose hypothesis carries provenance — captured sources, observed workflows, and the compared candidate set — without having to invent a segment/workflow hypothesis to satisfy the tool.

### Metric
Guided-discovery provenance coverage: the share of newly created investigations whose hypothesis links captured signals, explored candidates, and an explicit promotion decision.

### Baseline
0%. Investigation creation currently requires a supplied segment/workflow summary, and the only worked example is the seeded synthetic demo hypothesis (the accounting example in `seed.ts`), so no investigation has real discovery provenance.

### Target
100% of new dogfood investigations are created by promoting a compared candidate through the guided pre-hypothesis funnel with provenance attached.

### Time Horizon
End of the first Proofstack dogfood discovery cycle: EXP-002 recorded and BET-002 resolved to Validated or Killed.

### Guardrail Metrics
Zero synthetic or seeded demo records counted as market evidence; candidates remain explicitly unvalidated until promoted; promotion never marks a hypothesis validated by default.
