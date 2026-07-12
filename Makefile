.PHONY: help validate test verify demo metrics clean

PYTHON ?= python3

help:
	@$(PYTHON) scripts/ados.py --help

validate:
	@$(PYTHON) scripts/ados.py validate

test:
	@$(PYTHON) -m unittest discover -s tests -v

verify: validate test
	@echo "All governance gates passed."

demo:
	@$(PYTHON) scripts/ados.py demo

metrics:
	@$(PYTHON) scripts/ados.py metrics

clean:
	@rm -f observability/events/*.jsonl docs/metrics/latest.md
