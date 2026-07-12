# Assumptions

| ID | Assumption | Why It Matters | How to Test | Status |
| --- | --- | --- | --- | --- |
| A-001 | Teams will maintain upstream links when CI enforces them | Determines durability | Break a link and confirm validation fails | Validated |
| A-002 | Generated views avoid duplicate-source drift | Determines usability | Regenerate and compare deterministic output | Validated |
| A-003 | Extra product gates remain fast | Prevents bypass | Measure full local verification | Validated |
