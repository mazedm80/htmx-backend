#!/bin/bash

export API__PORT=8000
export API__DEBUG=True
export API__SECRET_KEY=""

export PSQL__HOST="mirserver"
export PSQL__PORT=5432
export PSQL__USER="htmx"
export PSQL__PASSWORD="htmx123"
export PSQL__DATABASE="pyhtmx"

python3 main.py