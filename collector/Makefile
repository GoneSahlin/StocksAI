PY = python3
VENV = venv
BIN=$(VENV)/bin

all: test

$(VENV): requirements.txt setup.py
	$(PY) -m venv $(VENV)
	$(BIN)/pip install -e .
	touch $(VENV)

.PHONY: test
test: $(VENV)
	$(PY) setup.py test

.PHONY: clean
clean:
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .eggs
	rm -rf collector.egg-info
	rm -rf geckodriver.log
