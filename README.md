# Implementação de idempotência em API bancária

# Sobre

Projeto de estudo sobre idempotência, no qual implemento utilizando o exemplo de contexto financeiro para garantir a segurança das transações impendindo de serem calculadas múltiplas vezes. Utilizado FastAPI para sua construção, a api possui autorização e autenticação com JWT e uso de refresh token, possui rotas para realizar uma transação, conferir o saldo, creditar um valor na conta (para fins de testes) e listar transações

# Como rodar

## Pré-requisitos

- Python 3.10+
- Docker e Docker Compose

1 - Clone o projeto
```bash
git clone https://github.com/gabrielferreira02/api_bancaria_fastapi.git
cd api_bancaria_fastapi
```

2 - Crie um arquivo .env na raiz com a seguinte forma
```env
DB_URL=postgresql://postgres:postgres@localhost:5432/apibanco
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
```


3 - Crie um ambiente virtual python
```bash
python3 -m venv venv
source venv/bin/activate # ou venv\Scripts\activate no Windows
```

4 - Instale as dependências
```bash
pip install -r requirements.txt
```

5 - Inicialize o banco de dados no docker
```bash
docker compose up -d
```

6 - Rode a migração
```bash
alembic upgrade head 
```

7 - Inicialize a API
```bash
fastapi dev app/main.py
```
8 - Acesse a documentação para testes em
```
http://localhost:8000/docs
```
