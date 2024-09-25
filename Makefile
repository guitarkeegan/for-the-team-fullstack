# Define common Docker Compose command
DOCKER_COMPOSE := docker compose

# Define profiles
FRONTEND_PROFILE := --profile frontend
BACKEND_PROFILE := --profile backend

# Frontend targets
.PHONY: front/up front/build front/up/build front/down
front/up:
	$(DOCKER_COMPOSE) $(FRONTEND_PROFILE) up

front/build:
	$(DOCKER_COMPOSE) $(FRONTEND_PROFILE) build

front/up/build:
	$(DOCKER_COMPOSE) $(FRONTEND_PROFILE) up --build

front/down:
	$(DOCKER_COMPOSE) $(FRONTEND_PROFILE) down

# Backend targets
.PHONY: back/up back/up/build back/down
back/up:
	$(DOCKER_COMPOSE) $(BACKEND_PROFILE) up

back/up/build:
	$(DOCKER_COMPOSE) $(BACKEND_PROFILE) up --build

back/down:
	$(DOCKER_COMPOSE) $(BACKEND_PROFILE) down -v

# Fullstack targets
.PHONY: fullstack/up fullstack/up/build fullstack/down
fullstack/up:
	$(DOCKER_COMPOSE) $(BACKEND_PROFILE) $(FRONTEND_PROFILE) up

fullstack/up/build:
	$(DOCKER_COMPOSE) $(BACKEND_PROFILE) $(FRONTEND_PROFILE) up --build

fullstack/down:
	$(DOCKER_COMPOSE) $(BACKEND_PROFILE) $(FRONTEND_PROFILE) down -v

# Maintenance targets
.PHONY: prune/all
prune/all:
	docker image prune -f 
	docker builder prune -f
	@echo "Pruned images and builder"
	@echo "Current processes:"
	docker system df

# Database migration target
.PHONY: db/migration/create
db/migration/create:
	@if [ -z "$(name)" ]; then \
		echo "Error: Please specify a migration name. Usage: make db/migration/create name=<name>"; \
		exit 1; \
	fi
	migrate create -ext sql -dir backend/migrations -seq $(name)