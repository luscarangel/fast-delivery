#!/bin/bash

echo "Executando migrations Alembic..."
alembic upgrade head

echo "Criando dados iniciais..."
python src/infra/db/seed.py

echo "Iniciando aplicação..."
exec "$@"