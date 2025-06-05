install:
	pip install --upgrade pip && pip install uv

test:
	 uv run python3 manage.py test

ruff:
	uv run ruff check

build:
	./build.sh

migrate:
	uv run python3 manage.py makemigrations && uv run python3 manage.py migrate

collectstatic:
	uv run python3 manage.py collectstatic --noinput --clear

render-start:
	gunicorn task_manager.wsgi

bootstrap:
	uv pip install django-bootstrap5

.PHONY:
	install
	test
	ruff
	build
	migrate
	collectstatic
	render-start
	start
	bootstrap
