# Assumptions

| ID | Assumption | Why It Matters | How to Test | Status |
| --- | --- | --- | --- | --- |
| A-001 | Teams will maintain upstream links when CI enforces them | Determines durability | Break a link and confirm validation fails | Validated |
| A-002 | Generated views avoid duplicate-source drift | Determines usability | Regenerate and compare deterministic output | Validated |
| A-003 | Extra product gates remain fast | Prevents bypass | Measure full local verification | Validated |
| A-004 | Real Proofstack sessions start from raw signals, not a formed segment/workflow hypothesis | If false, the pre-hypothesis funnel is ceremony and BET-002 should be killed | In EXP-002, record whether each dogfood exploration starts with signals or an already-formed hypothesis | Open |
| A-005 | Provenance attached at promotion keeps unvalidated and synthetic inputs from being treated as validation | Protects evidence integrity through validate, experiment, and productize | Promote a candidate in EXP-002 and inspect that the investigation shows its sources, compared candidates, and an explicit unvalidated status | Open |
| A-006 | Comparing several candidates changes which hypothesis gets investigated | Confirms the funnel adds decision value beyond record keeping | In EXP-002, record the initial hunch and whether the promoted candidate differs after comparison | Open |
