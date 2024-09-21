.PHONY: front/up
	docker compose --profile frontend up

.PHONY: front/build
	docker compose --profile frontend build

.PHONY: front/up/build
	docker compose --profile frontend up --build

.PHONY: front/down
	docker compose --profile frontend down

.PHONY: back/up
	docker compose --profile backend up

.PHONY: back/up/build
	docker compose --profile backend up --build

.PHONY: fullstack/up
	docker compose --profile backend --profile frontend up

.PHONY: fullstack/up/build
	docker compose --profile backend --profile frontend up --build

.PHONY: back/down
	docker compose --profile backend down -v

.PHONY: prune/all
	docker image prune -y
	docker builder prune -y
	@echo "pruned images and builder"
	@echo "current processes"
	docker system df

# Define the target with a variable
.PHONY: db/migration/create

# Target for creating a new migration
db/migration/create:
	@if [ -z "$(name)" ]; then echo "Error: Please specify a migration name. Usage: make db/migration/create name=<name>"; exit 1; fi
	migrate create -ext sql -dir backend/migrations -seq $(name)