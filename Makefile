.PHONY: dev lint format test

dev:
	streamlit run streamlit_app.py

lint:
	ruff check .

format:
	ruff format .

test:
	pytest -q 