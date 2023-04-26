VENV="collector/.collector-venv"


all: test lint

$(VENV): pyproject.toml setup.cfg
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -e .[dev]
	touch $(VENV)

.PHONY: test
test: $(VENV)
	$(VENV)/bin/pytest

.PHONY: test-collector
test-collector: $(VENV)
	$(VENV)/bin/pytest collector/

.PHONY: test-model
test-model: $(VENV)
	$(VENV)/bin/pytest model/

.PHONY: train
train: $(VENV)
	$(VENV)/bin/python3 model/train.py

.PHONY: collect
collect: $(VENV)
	$(VENV)/bin/python3 collector/historical.py

.PHONY: lint
lint: $(VENV)
	-$(VENV)/bin/flake8 --exclude $(VENV)

.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .eggs
	rm -rf collector.egg-info
	rm -rf geckodriver.log
