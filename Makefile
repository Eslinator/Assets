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

# --- extras ---
.PHONY: resolve-all plans-all serve new-asset

resolve-all: deps
	. .venv/bin/activate && \
	for a in $$(ls kb/assets); do \
	  python tools/resolve_asset.py $$a > kb/index/resolved/$$a.json; \
	done
	@echo "Resolved all assets into kb/index/resolved/"

plans-all: deps
	. .venv/bin/activate && \
	for f in kb/index/resolved/*.json; do \
	  python tools/make_plan.py "$$f"; \
	done
	@echo "Plans written to ./plans"

serve:
	python3 -m http.server 8787 -d kb/index

# usage: make new-asset ID=something PURPOSE="..." TRIS=1200 TEX=512 TIER=background
new-asset:
	./tools/new_asset.sh "$(ID)" "$(PURPOSE)" "$(TRIS)" "$(TEX)" "$(TIER)"
	@echo "Next: . .venv/bin/activate && python tools/resolve_asset.py $(ID) > kb/index/resolved/$(ID).json && python tools/make_plan.py kb/index/resolved/$(ID).json"
