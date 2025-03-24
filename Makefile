# Makefile for GenAI IPE Project

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements-dev.txt

venv:
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

run-ui:
	streamlit run streamlit_ui.py

docker-build:
	docker build -t genai-ipe .

docker-run:
	docker run -p 8501:8501 genai-ipe

compose-up:
	docker-compose up --build

compose-down:
	docker-compose down
