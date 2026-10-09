PYTHON ?= python3

.PHONY: test verify-json verify-shell verify-repository verify verify-final

test:
	$(PYTHON) -m pytest -q

verify-json:
	$(PYTHON) -c 'import json,pathlib; [json.loads(p.read_text()) for p in pathlib.Path(".").rglob("*.json") if ".git" not in p.parts and ".superpowers" not in p.parts]'

verify-shell:
	bash -n production/*.sh

verify-repository:
	$(PYTHON) scripts/verify_repository.py --pre-publication

verify: test verify-json verify-shell verify-repository

verify-final: test verify-json verify-shell
	$(PYTHON) scripts/verify_repository.py
