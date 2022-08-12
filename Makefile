install:
	poetry install
lint:
	poetry run flake8 task_manager
selfcheck:
	poetry check
check: selfcheck lint