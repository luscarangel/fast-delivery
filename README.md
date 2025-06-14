# FastDelivery API

Esta API simula o gerenciamento de entregadores e pedidos, incluindo controle de status de entrega, usando **FastAPI** e arquitetura limpa, com suporte a banco de dados, testes automatizados, e deploy na AWS

## Tecnologias utilizadas

- FastAPI + Pydantic
- PostgreSQL + SQLAlchemy
- Alembic
- Docker + Docker Compose
- GitHub Actions
- Pytest + Linting (black, isort, flake8)

## Funcionalidades
- Criação, listagem, atualização e remoção de Entregadores
- Criação, listagem, atualização e remoção de Pedidos
- Atribuição de entregador a pedido
- Atualização do status de entrega
- Health check e métricas com Prometheus

## Estrutura do projeto
```
alembic/        # Migrations
core/           # Configurações
terraform/      # IaC
src/
├── api/        # Rotas e controllers
├── domain/     # Entidades e interfaces
├── infra/      # Modelos, repositórios, Database
├── tests/      # Testes unitários e integração
└── use_cases/  # Regras de negócio
```

## Executando localmente

1. Clone o repositório
2. Crie um ambiente virtual e ative:
```bash
# Linux
python3 -m venv .venv
source .venv/bin/activate
```
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
```
3. Instale as dependências:
```bash
pip install -r requirements-dev.txt
```
4. Crie o arquivo `.env` a partir do exemplo:
```bash
cp .env.example .env
```
5. Se necessário, personalize as variáveis de ambiente em `.env`
6. Execute com Docker Compose:
```bash
docker compose up --build -d
```

Acesse a API em: http://localhost:8000

### Testes e Lint
Execute os comandos:
```bash
pytest                # Executa os testes unitários e integração
black --check .       # Formata o código
isort --check-only .  # Organiza imports
flake8 .              # Linting
```

## Endpoints principais
| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Health check da API |
| GET | `/metrics` | Métricas Prometheus |
| GET | `/api/v1/couriers` | Listar entregadores |
| POST | `/api/v1/orders` | Criar novo pedido |
| GET | `/api/v1/orders` | Listar pedidos |
| PUT | `/api/v1/orders/{id}` | Atualizar um pedido |
| DELETE | `/api/v1/orders/{id}` | Deletar um pedido |

Documentação Swagger completa: http://localhost:8000/docs

## Esteira CI/CD
Configuração via GitHub Actions em `.github/workflows`
- Pipeline executado a cada push/pull request para a master
- Roda testes unitários e de integração
- Valida o código com lint
- Constrói a infraestrutura cloud
- Faz deploy para AWS