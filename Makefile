SHELL := /bin/bash

VENV = collector/.collector-venv
CONDA_ENV_NAME ?= model/stocksai-model-env
ACTIVATE_ENV = source ~/miniconda3/bin/activate ./$(CONDA_ENV_NAME)

all: test lint

.PHONY: test
test: test-collector

.PHONY: lint
lint: $(VENV)
	-$(VENV)/bin/flake8 --exclude $(VENV)

$(VENV): collector/pyproject.toml collector/setup.cfg
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -e collector[dev]
	touch $(VENV)

.PHONY: test-collector
test-collector: $(VENV)
	$(VENV)/bin/pytest collector

.PHONY: collect
collect: $(VENV)
	$(VENV)/bin/python3 collector/historical.py

.PHONY: build-conda-env
build-conda-env: $(CONDA_ENV_NAME)
$(CONDA_ENV_NAME): model/pyproject.toml model/setup.cfg
	# create conda environment
	conda create -p $(CONDA_ENV_NAME) --copy -y python=3.9

	# install for tensorflow gpu
	$(ACTIVATE_ENV) && conda install -y -c conda-forge cudatoolkit=11.8.0 &&\
	pip install nvidia-cudnn-cu11==8.6.0.163 &&\
	mkdir -p ./$(CONDA_ENV_NAME)/etc/conda/activate.d &&\
	echo 'CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))' >> ./$(CONDA_ENV_NAME)/etc/conda/activate.d/env_vars.sh &&\
	echo 'export LD_LIBRARY_PATH=$(LD_LIBRARY_PATH):,.$(CONDA_ENV_NAME)/lib/:$(CUDNN_PATH)/lib' >> ./$(CONDA_ENV_NAME)/etc/conda/activate.d/env_vars.sh

	# install module
	$(ACTIVATE_ENV) && pip install --upgrade pip &&\
	pip install -e model[dev]

	# fix for ubuntu
	$(ACTIVATE_ENV) && conda install -y -c nvidia cuda-nvcc=11.3.58 &&\
	printf 'export XLA_FLAGS=--xla_gpu_cuda_data_dir=./$(CONDA_ENV_NAME)/lib/\n' >> ./$(CONDA_ENV_NAME)/etc/conda/activate.d/env_vars.sh &&\
	source ./$(CONDA_ENV_NAME)/etc/conda/activate.d/env_vars.sh &&\
	mkdir -p ./$(CONDA_ENV_NAME)/lib/nvvm/libdevice &&\
	cp ./$(CONDA_ENV_NAME)/lib/libdevice.10.bc ./$(CONDA_ENV_NAME)/lib/nvvm/libdevice/

.PHONY: test-model
test-model:
	$(ACTIVATE_ENV) && pytest model -s

.PHONY: train
train: $(CONDA_ENV_NAME)
	$(ACTIVATE_ENV) && python model/src/train.py

.PHONY: clean-conda-env
clean-conda-env:
	rm -rf $(CONDA_ENV_NAME)

.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .eggs
	rm -rf collector/stocksai_collector.egg-info
	rm -rf geckodriver.log
	rm -rf collector/.pytest_cache
