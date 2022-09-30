SHELL := /bin/bash
.SHELLFLAGS = -ec
.ONESHELL:
.SILENT:

.EXPORT_ALL_VARIABLES:
REPO_DIRECTORY:=$(shell pwd)

.PHONY: help
help:
	echo "❓ Use \`make <target>\`"
	grep -E '^\.PHONY: [a-zA-Z0-9_-]+ .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: graphviz  ## 🛠️Install graphviz
graphviz:
	apt update & apt install graphviz -y

.PHONY: dependencies  ## 🛠️Install dependencies
dependencies:
	pip install -r requirements.txt

