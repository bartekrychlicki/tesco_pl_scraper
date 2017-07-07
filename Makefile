.PHONY: help install

help:
	@cat README.md

install:
	./ubuntu_deps.sh
	pip install -r requirements.txt
