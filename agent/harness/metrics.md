# Metric Contract

Events follow `observability/schema/event.schema.json`. The local event store is append-only JSON Lines. Required lifecycle events are `loop.started`, `verification.completed`, and `loop.stopped`.

Metrics are aggregated by `python scripts/ados.py metrics`. Do not optimize a throughput metric without reviewing regression, intervention, and outcome measures alongside it.
