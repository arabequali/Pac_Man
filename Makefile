install:
	uv sync

run:
	uv run python3 pac-man.py config.json

debug:
	echo "test"

clean:
	@rm -rf src/__pycache__/

lint:
	uv run python3 -m mypy .