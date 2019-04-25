all: install compile-sass quality test

install-test:
	pip install -q -r test_requirements.txt

install: install-test

quality:
	./scripts/quality.sh

test:
	./scripts/test.sh
