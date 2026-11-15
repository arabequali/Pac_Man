install:
	uv sync

run:
	uv run python3 pac-man.py config.json

debug:
	echo "test"

clean:
	@rm -rf src/__pycache__/

lint:
		uv run python3 -m flake8 .
		uv run python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs