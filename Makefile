install:
	pip install --upgrade pip && pip install uv

test:
	uv run pytest

#lint:
#	poetry run flake8 page_analyzer

ruff:
	uv run ruff check

selfcheck:
	uv check

check: 
	selfcheck test lint

build:
	./build.sh

# publish:
# 	uv publish --dry-run

# package-install:
# 	python3 -m pip install --user dist/*.whl

#dev:
#	poetry run flask --app page_analyzer:app run --debug
migrate:
	uv run python3 manage.py migrate

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
#	lint
	selfcheck
	check
	build
#	publish
#	package-install
#	start
#	dev
	migrate
	collectstatic
	render-start
	start
	bootstrap
