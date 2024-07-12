MANAGER_TAG="tg-groups-manager"
MANAGER_DOCKERFILE_CONTEXT="manager/"
PARSER_TAG="tg-groups-parser"
PARSER_DOCKERFILE_CONTEXT="parser/"

bm:
	@echo "Building manager image..."
	docker build -t $(MANAGER_TAG) $(MANAGER_DOCKERFILE_CONTEXT)

bp:
	@echo "Building parser image..."
	docker build -t $(PARSER_TAG) $(PARSER_DOCKERFILE_CONTEXT)
