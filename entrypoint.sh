#!/bin/bash

if [ "$ENV" = "development" ]; then
  echo "Executando migrations Alembic (modo desenvolvimento)..."
  alembic upgrade head
fi

echo "Executando seed..."
python src/infra/db/seed.py

echo "Iniciando aplicação..."
exec "$@"