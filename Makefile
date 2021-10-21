export DISCORD_MOUSE_BOT_VERSION=$$(git rev-parse --short HEAD)
export DISCORD_MOUSE_BOT_IMAGE="discord-mouse-bot:${DISCORD_MOUSE_BOT_VERSION}"

build:
	rm -rf docker/target
	mkdir -p docker/target
	cp -r requirements.txt src docker/target
	cd docker && docker build --rm -t ${DISCORD_MOUSE_BOT_IMAGE} .
	docker tag ${DISCORD_MOUSE_BOT_IMAGE} discord-mouse-bot:latest
