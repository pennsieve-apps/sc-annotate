.PHONY: help test fixture run clean validate

SERVICE_NAME ?= sc-annotate
PYTHON ?= python3
export DOCKER_DEFAULT_PLATFORM = linux/amd64

.DEFAULT: help

help:
	@echo "Make Help for $(SERVICE_NAME)"
	@echo ""
	@echo "make test      - pytest: the synthetic fixture through every mode and both input layouts (no Docker)"
	@echo "make fixture   - write the synthetic sc-integrate output, reference and markers.csv to data/fixture/{linked,flat}/"
	@echo "make run       - build the cpu image and run it in Docker over data/fixture/linked/ into data/output/"
	@echo "make validate  - app.yml against the manifest schema, CITATION.cff with cffconvert"
	@echo "make clean     - remove data/output/"
	@echo ""
	@echo "PYTHON=$(PYTHON) (set PYTHON=.venv/bin/python after pip install -r requirements-dev.txt)"

test:
	$(PYTHON) -m pytest -q tests

fixture:
	$(PYTHON) -m tests.make_fixture data/fixture

run: clean fixture
	mkdir -p data/output
	docker compose -f docker-compose.yml down --remove-orphans
	docker compose -f docker-compose.yml build
	docker compose -f docker-compose.yml up --exit-code-from processor
	docker compose -f docker-compose.yml down --remove-orphans
	@echo "--- outputs:"
	@find data/output -type f | sort

validate:
	$(PYTHON) -c "import json, yaml, jsonschema; s = json.load(open('../workflow-single-cell/docs/app-manifest.v1.schema.json')); jsonschema.validate(yaml.safe_load(open('app.yml')), s); print('app.yml ok')"
	$(dir $(PYTHON))cffconvert --validate && echo "CITATION.cff ok"

clean:
	rm -rf data/output
