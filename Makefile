# Platform details
OS              := $(shell uname | tr A-Z a-z)
ARCH            := $(shell uname -m)
PLATFORM        := $(ARCH)-$(OS)

PYTHON ?= python3


all: setup dev-no-log ## Install dependencies and run in dev mode.


.PHONY: setup
setup: ## Install dependencies.
	python3 -m venv .venv
	./.venv/bin/python -m pip install --upgrade pip
	./.venv/bin/python -m pip install -r requirements.txt


.PHONY: clean
clean: ## Remove virtual environment and user data.
	rm -rf app-data
	rm -rf .venv poetry.lock .pytest_cache h2o_wave.state
	find . -type d -name "__pycache__" -exec rm -rf \;


.PHONY: run
run: ## Run the app with no reload.
	./.venv/bin/wave run --no-reload demo_app/app.py


.PHONY: run-no-log
run-no-log: ## Run the app with no reload and with no logs from wave server.
	H2O_WAVE_NO_LOG=True ./.venv/bin/wave run --no-reload demo_app/app.py


.PHONY: dev
dev: ## Run the app with active reload.
	./.venv/bin/wave run demo_app/app.py


.PHONY: dev-no-log
dev-no-log: ## Run the app with active reload, but not with logs from wave server.
	H2O_WAVE_NO_LOG=True ./.venv/bin/wave run demo_app/app.py


.PHONY: help
help: ## List all make tasks.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
