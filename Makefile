.DEFAULT_GOLAD := help

run: ## start server
	docker-compose up -d
	poetry run gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker -c app/infrastructure/gunicorn.conf.py

add:
	poetry add $(LIBRARY)

remove:
	poetry remove $(LIBRARY)

help: ## help command
	@echo "Help"

migrate-create:
	poetry run alembic revision --autogenerate -m "$(D)"

migrate-apply:
	poetry run alembic upgrade head

migrate-downgrade:
	poetry run alembic downgrade base $(HASH)

migrate-reset:
	poetry run alembic downgrade base

migrate-restart:
	make migrate-reset
	make migrate-apply

test:
	poetry run pytest tests