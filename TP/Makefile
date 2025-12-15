# Variables
PYTHON = python
PYTEST = $(PYTHON) -m pytest
RUFF = $(PYTHON) -m ruff
PDOC = $(PYTHON) -m pdoc

.PHONY: all unit_test perf_test coverage lint doc clean

all: lint unit_test coverage

# 1. Tests Unitaires & Intégration
unit_test:
	$(PYTEST) tests/unit tests/integration -v

# 2. Tests de Performance
perf_test:
	$(PYTEST) tests/performance -v

# 3. Couverture de Code
coverage:
	$(PYTEST) --cov=triangulator tests/ --cov-report=html --cov-report=term

# 4. Qualité de Code
lint:
	$(RUFF) check .

# 5. Documentation
doc:
	$(PDOC) --html --output-dir docs triangulator --force

# Nettoyage
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf docs
