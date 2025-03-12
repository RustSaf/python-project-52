install:
	pip install --upgrade pip && uv install

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

publish:
	uv publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

#dev:
#	poetry run flask --app page_analyzer:app run --debug
migrate:
	python3 manage.py migrate

collectstatic:
	python manage.py collectstatic

render-start:
	gunicorn task_manager.wsgi

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

.PHONY:
	install
	test
	ruff
#	lint
	selfcheck
	check
	build
	publish
	package-install
#	start
#	dev
	migrate
	collectstatic
	render-start
	start
