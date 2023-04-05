all: test lint

.venv: pyproject.toml setup.cfg
	python3 -m venv .venv
	.venv/bin/pip install -e .[dev]
	touch .venv

.PHONY: test
test: .venv
	.venv/bin/pytest

.PHONY: test-collector
test-collector: .venv
	.venv/bin/pytest collector/

.PHONY: test-model
test-model: .venv
	.venv/bin/pytest model/

.PHONY: train
train: .venv
	.venv/bin/python3 model/train.py

.PHONY: lint
lint: .venv
	-.venv/bin/flake8 --exclude .venv

.PHONY: clean
clean:
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .eggs
	rm -rf collector.egg-info
	rm -rf geckodriver.log
