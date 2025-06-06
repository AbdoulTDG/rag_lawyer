venv:
	uv venv

install:
	uv pip install -r requirements.txt

build:
	docker-compose build --up

