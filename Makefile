install:
	pip install --upgrade pip && pip install uv

test:
	uv run pytest

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

#PORT ?= 8000
#start:
#	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

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
