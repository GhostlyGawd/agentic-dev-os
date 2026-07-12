.PHONY: help validate test lint verify demo metrics dashboard audit clean

PYTHON ?= python3

help:
	@$(PYTHON) scripts/ados.py --help

validate:
	@$(PYTHON) scripts/ados.py validate

test:
	@$(PYTHON) -m unittest discover -s tests -v

lint:
	@$(PYTHON) -m compileall -q src scripts ci tests
	@$(PYTHON) ci/lint.py

verify: lint validate test
	@echo "All governance gates passed."

demo:
	@$(PYTHON) scripts/ados.py demo

metrics:
	@$(PYTHON) scripts/ados.py metrics

dashboard: metrics

audit:
	@$(PYTHON) scripts/ados.py audit-stale

clean:
	@rm -f observability/events/*.jsonl docs/metrics/latest.md
