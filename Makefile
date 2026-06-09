PYTHON ?= python3
INPUT_FILE ?= data/raw/customers.csv
OUTPUT_FILE ?= data/processed/customers_processed.csv
REPORT_FILE ?= reports/pipeline_summary.md

.PHONY: install lint test run clean validate

install:
	$(PYTHON) -m pip install -r requirements.txt -r requirements-dev.txt

lint:
	$(PYTHON) -m ruff check .

test:
	$(PYTHON) -m pytest -v

run:
	PYTHONPATH=src $(PYTHON) -m dataops_pipeline.pipeline \
		--input $(INPUT_FILE) \
		--output $(OUTPUT_FILE) \
		--report $(REPORT_FILE)

clean:
	rm -f data/processed/*.csv
	rm -f reports/*.md

validate: lint test run
