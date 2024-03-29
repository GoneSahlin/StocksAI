SHELL := /bin/bash

COL_VENV = collector/.venv
APP_VENV = app/.venv

# CONDA_ENV_NAME ?= model/stocksai-model-env
# CONDA_ENV_NAME ?= tf
# ACTIVATE_ENV = source ~/miniconda3/bin/activate ./$(CONDA_ENV_NAME)

all: test lint

.PHONY: test
test: test-collector

.PHONY: lint
lint: $(COL_VENV)
	-$(COL_VENV)/bin/flake8 --exclude $(COL_VENV) --exclude $(COL_VENV)

# -------------- COLLECTOR ---------------
$(COL_VENV): collector/pyproject.toml collector/setup.cfg
	python3 -m venv $(COL_VENV)
	$(COL_VENV)/bin/pip install -e collector[dev]
	touch $(COL_VENV)

.PHONY: test-collector
test-collector: $(COL_VENV)
	$(COL_VENV)/bin/pytest collector

.PHONY: collect
collect: $(COL_VENV)
	$(COL_VENV)/bin/python3 collector/src/historical.py
	
# ---------------- LAMBDA ----------------
collect_lambda.zip: FORCE
	rm -f collect_lambda.zip
	python3 -m venv .lambda-venv
	.lambda-venv/bin/pip install ./collector
	cd .lambda-venv/lib/python3.10/site-packages &&\
	zip -r ../../../../collect_lambda.zip .
	cd lambdas &&\
	zip -g ../collect_lambda.zip collect.py
	rm -rf .lambda-venv

# ----------------- APP ------------------
$(APP_VENV): app/pyproject.toml app/setup.cfg
	python3 -m venv $(APP_VENV)
	$(APP_VENV)/bin/pip install -e utils[dev]
	$(APP_VENV)/bin/pip install -e app[dev]
	touch $(APP_VENV)

.PHONY: run-app
run-app: $(APP_VENV)
	cd app/src/ &&\
	../../$(APP_VENV)/bin/streamlit run app.py


# .PHONY: build-conda-env
# build-conda-env: $(CONDA_ENV_NAME)
# $(CONDA_ENV_NAME): model/pyproject.toml model/setup.cfg
# 	# create conda environment
# 	conda create -p $(CONDA_ENV_NAME) --copy -y python=3.9

# 	# install for tensorflow gpu
# 	$(ACTIVATE_ENV) && conda install -y -c conda-forge cudatoolkit=11.8.0 &&\
# 	pip install nvidia-cudnn-cu11==8.6.0.163 &&\
# 	mkdir -p ./$(CONDA_ENV_NAME)/etc/conda/activate.d &&\
# 	echo 'CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))' >> ./$(CONDA_ENV_NAME)/etc/conda/activate.d/env_vars.sh &&\
# 	echo 'export LD_LIBRARY_PATH=$(LD_LIBRARY_PATH):,.$(CONDA_ENV_NAME)/lib/:$(CUDNN_PATH)/lib' >> ./$(CONDA_ENV_NAME)/etc/conda/activate.d/env_vars.sh

# 	# install module
# 	$(ACTIVATE_ENV) && pip install --upgrade pip &&\
# 	pip install -e model[dev]

# 	# fix for ubuntu
# 	$(ACTIVATE_ENV) && conda install -y -c nvidia cuda-nvcc=11.3.58 &&\
# 	printf 'export XLA_FLAGS=--xla_gpu_cuda_data_dir=./$(CONDA_ENV_NAME)/lib/\n' >> ./$(CONDA_ENV_NAME)/etc/conda/activate.d/env_vars.sh &&\
# 	source ./$(CONDA_ENV_NAME)/etc/conda/activate.d/env_vars.sh &&\
# 	mkdir -p ./$(CONDA_ENV_NAME)/lib/nvvm/libdevice &&\
# 	cp ./$(CONDA_ENV_NAME)/lib/libdevice.10.bc ./$(CONDA_ENV_NAME)/lib/nvvm/libdevice/

# .PHONY: test-model
# test-model:
# 	$(ACTIVATE_ENV) && pytest model -s

# .PHONY: train
# train:
# 	$(ACTIVATE_ENV) && python model/src/train.py

# .PHONY: clean-conda-env
# clean-conda-env:
# 	rm -rf $(CONDA_ENV_NAME)

.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .eggs
	rm -rf collector/stocksai_collector.egg-info
	rm -rf geckodriver.log
	rm -rf collector/.pytest_cache
	rm collect_lambda.zip

FORCE:
