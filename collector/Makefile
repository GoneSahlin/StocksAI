.venv: requirements.txt setup.py
	python3 -m venv .venv
	.venv/bin/pip install -e .
	touch .venv

.PHONY: test
test: .venv
	python3 setup.py test

.PHONY: clean
clean:
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .eggs
	rm -rf collector.egg-info
	rm -rf geckodriver.log
