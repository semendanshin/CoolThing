MANAGER_TAG="tg-groups-manager"
MANAGER_DOCKERFILE_CONTEXT="manager/"
PARSER_TAG="tg-groups-parser"
PARSER_DOCKERFILE_CONTEXT="parser/"
NETWORK_NAME="coolthing_bridge"

bm:
	@echo "Building manager image..."
	docker build -t $(MANAGER_TAG) $(MANAGER_DOCKERFILE_CONTEXT)

bp:
	@echo "Building parser image..."
	docker build -t $(PARSER_TAG) $(PARSER_DOCKERFILE_CONTEXT)

mn:
	@echo "Creating network..."
	docker network create --driver bridge $(NETWORK_NAME)

gp:
	git add $(s)
	git status
	git commit -m "$(m)"
	git push origin $(b)

deploy:
	docker compose stop
	git pull origin $(b)
	docker compose up --build -d
	docker compose stop scripts
	docker compose up --build scripts -d