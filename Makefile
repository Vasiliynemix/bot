init:
	alembic init -t async src/db/migrations

generate:
	alembic revision --m "$(name)" --autogenerate

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade $(id)