install:
	poetry install
lint:
	poetry run flake8 task_manager
test:
	poetry run pytest
selfcheck:
	poetry check
check: selfcheck test lint