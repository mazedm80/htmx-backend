#!/bin/bash
docker run \
  --name pyhtmx \
  --restart always \
  -p 8000:80 \
  -e MAX_WORKERS=2 \
  -e PSQL__HOST="mirserver" \
  -e PSQL__PORT=5432 \
  -e PSQL__USER="htmx" \
  -e PSQL__PASSWORD="htmx123" \
  -e PSQL__DATABASE="pyhtmx" \
	-d pyhtmx:latest