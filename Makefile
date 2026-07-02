.PHONY: up bootstrap down logs clean ps

up:
	docker compose up -d

bootstrap:
	docker compose up -d
	docker compose \
		-f docker-compose.yml \
		-f docker-compose.bootstrap.yml \
		run --rm minio-bootstrap

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

clean:
	docker compose down -v