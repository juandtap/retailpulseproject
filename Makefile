.PHONY: up down bootstrap spark-up spark-down spark-run spark-status spark-logs ps clean

up:
	docker compose up -d

bootstrap:
	docker compose up -d
	docker compose \
		-f docker-compose.yml \
		-f docker-compose.bootstrap.yml \
		run --rm minio-bootstrap

spark-up:
	docker compose \
		-f docker-compose.yml \
		-f docker-compose.spark.yml \
		up -d 

spark-down:
	docker compose \
		-f docker-compose.yml \
		-f docker-compose.spark.yml \
		stop spark-master spark-worker

spark-run:
	docker exec -it \
		-w /opt/retailpulse/spark-processor \
		-e PYTHONPATH=/opt/retailpulse/spark-processor \
		retailpulse-spark-master \
		/opt/spark/bin/spark-submit \
		app/main.py

spark-status:
	docker compose \
		-f docker-compose.yml \
		-f docker-compose.spark.yml \
		ps spark-master spark-worker

spark-logs:
	docker compose \
		-f docker-compose.yml \
		-f docker-compose.spark.yml \
		logs -f spark-master spark-worker

ps:
	docker compose \
		-f docker-compose.yml \
		-f docker-compose.spark.yml \
		ps

down:
	docker compose \
		-f docker-compose.yml \
		-f docker-compose.spark.yml \
		down

clean:
	docker compose \
		-f docker-compose.yml \
		-f docker-compose.spark.yml \
		down -v --remove-orphans