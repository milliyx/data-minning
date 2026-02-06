.PHONY: help setup clean generate pipeline features train evaluate all test lint

TEAM ?= configs/teams/team01.yaml
RUN_DATE ?= 2026-02-01
PYTHON := python

help:
	@echo "Minería de Datos - Lakehouse Template"
	@echo ""
	@echo "Usage: make [target] TEAM=<team_config> RUN_DATE=<date>"
	@echo ""
	@echo "Targets:"
	@echo "  setup      - Install dependencies and prepare environment"
	@echo "  clean      - Remove generated data"
	@echo "  generate   - Generate raw data (Bronze layer)"
	@echo "  pipeline   - Run ETL pipeline (Bronze->Silver->Gold)"
	@echo "  features   - Build ML features"
	@echo "  train      - Train all models"
	@echo "  evaluate   - Generate evaluation reports"
	@echo "  all        - Run complete pipeline (generate+pipeline+features+train+evaluate)"
	@echo "  test       - Run test suite"
	@echo "  lint       - Run code quality checks"
	@echo ""
	@echo "Examples:"
	@echo "  make setup"
	@echo "  make all TEAM=configs/teams/team01.yaml RUN_DATE=2026-02-01"
	@echo "  make generate TEAM=configs/teams/team02.yaml RUN_DATE=2026-02-01"

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"
	@echo "Setup complete! Data directories will be created on first run."

clean:
	rm -rf data/bronze data/silver data/gold
	rm -rf src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	@echo "Cleaned data and cache directories"

generate:
	$(PYTHON) -m md_lakehouse.cli generate --team $(TEAM) --run-date $(RUN_DATE)

pipeline:
	$(PYTHON) -m md_lakehouse.cli pipeline --team $(TEAM) --run-date $(RUN_DATE)

features:
	$(PYTHON) -m md_lakehouse.cli features --team $(TEAM) --run-date $(RUN_DATE)

train:
	$(PYTHON) -m md_lakehouse.cli train --team $(TEAM) --run-date $(RUN_DATE)

evaluate:
	$(PYTHON) -m md_lakehouse.cli evaluate --team $(TEAM) --run-date $(RUN_DATE)

all:
	$(PYTHON) -m md_lakehouse.cli all --team $(TEAM) --run-date $(RUN_DATE)

test:
	$(PYTHON) -m pytest tests/ -v --cov=src/md_lakehouse --cov-report=term-missing

lint:
	$(PYTHON) -m ruff check src/ tests/
	$(PYTHON) -m ruff format --check src/ tests/
