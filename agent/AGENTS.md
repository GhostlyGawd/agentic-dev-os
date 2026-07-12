# Agent Rules

These rules apply to every automated loop in this repository.

1. Read `.ai/` orientation and every outcome, opportunity, bet, milestone, PRD, spec, and policy linked by the active ticket.
2. Work on one ticket only.
3. Change only paths listed under `Files Allowed`.
4. Stop and request review if the task is ambiguous, cross-cutting, irreversible, security-sensitive, or outside scope.
5. Update tests and traceability in the same change as behavior.
6. Emit `loop.started`, `verification.completed`, and `loop.stopped` events.
7. Run `make verify` before declaring completion.
8. Never expose secrets, bypass a failed gate, or silently weaken a policy.
9. Stop when acceptance criteria are satisfied.
10. Do not create a PRD from conversation; require a validated bet or approved change request.
11. Never edit `.ai/requirements/` generated views directly.

Definition of done: acceptance criteria pass, trace status is current, completion notes exist, verification evidence is recorded, and the loop has stopped.
