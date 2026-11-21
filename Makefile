RUN    ?= uv run
CONFIG ?= config.json
MAIN    = pac-man.py

MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
             --disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint lint-strict test

install:
	uv sync

run:
	$(RUN) python3 $(MAIN) $(CONFIG)

debug:
	$(RUN) python3 -m pdb $(MAIN) $(CONFIG)

clean:
	find . -name .venv -prune -o -type d \
		\( -name __pycache__ -o -name .mypy_cache -o -name .pytest_cache \) \
		-exec rm -rf {} +
	rm -rf build dist

lint:
	$(RUN) python3 -m flake8 .
	$(RUN) python3 -m mypy . $(MYPY_FLAGS)

lint-strict:
	$(RUN) python3 -m flake8 .
	$(RUN) python3 -m mypy . --strict

test:
	$(RUN) python3 -m pytest tests