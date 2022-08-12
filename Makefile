install:
	poetry install
lint:
	poetry run flake8 page_loader
test:
	poetry run pytest
selfcheck:
	poetry check
check: selfcheck test lint