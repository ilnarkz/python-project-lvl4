install:
	poetry install
lint:
	poetry run flake8 task_manager
check:
	poetry check
start:
	poetry run python manage.py runserver 0.0.0.0:8000
migrate:
	poetry run python manage.py migrate
deploy:
	git push heroku main