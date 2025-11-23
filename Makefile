.PHONY: venv deps validate import publish

venv:
	python3 -m venv .venv

deps: venv
	. .venv/bin/activate && pip install -r tools/requirements.txt

validate: deps
	. .venv/bin/activate && python tools/kb_import.py kb/bundles/kb_bundle_v1.json >/dev/null || exit 1
	@echo "Schema & import validation passed (dry run)."

import: deps
	. .venv/bin/activate && python tools/kb_import.py kb/bundles/kb_bundle_v1.json

publish:
	git add kb tools Makefile && git commit -m "Import KB bundle v1" || true
