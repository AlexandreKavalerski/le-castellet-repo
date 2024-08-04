down:
	docker compose down
down-rm:
	docker compose down --rmi local
up:
	docker compose up -d

up-build:
	docker compose up -d --build
local:
	uvicorn src.app.main:app --host 0.0.0.0 --port 8005 --reload

transcriptions:
	python -m src.app.commands.transcribe_mentorships
summaries:
	python -m src.app.commands.summarize_mentorships
details:
	python -m src.app.commands.other_info_mentorships

migration_up:
	cd src/ && alembic upgrade head
migration_down:
	cd src/ && alembic downgrade head-$(rollback)