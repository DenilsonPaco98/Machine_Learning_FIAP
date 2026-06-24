.PHONY: help install lint test run-api train clean test-smoke

help:
	@echo "Tech Challenge - Makefile Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make lint       - Run ruff linter"
	@echo "  make test       - Run tests with coverage"
	@echo "  make test-smoke - Run smoke tests only"
	@echo "  make run-api    - Start FastAPI server"
	@echo "  make train      - Train model pipeline"
	@echo "  make clean      - Clean temporary files"

install:
	pip install -r requirements.txt
	pip install -e .

lint:
	ruff check src tests scripts

test:
	pytest tests/ -v --cov=src --cov-report=html

test-smoke:
	pytest tests/test_smoke.py -v

run-api:
	python -m uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000

train:
	python scripts/train_pipeline.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".ruff_cache" -delete
	find . -type d -name "htmlcov" -delete
	rm -rf dist/ build/ *.egg-info/
	rm -rf .coverage

	# Security / Quality targets
	sonar-local:
		@echo "Executando Sonar Scanner localmente (requer sonar-scanner instalado)"
		sonar-scanner

	semgrep-local:
		@echo "Executando Semgrep local via Docker"
		docker run --rm -v $(PWD):/src -w /src returntocorp/semgrep semgrep --config p/ci

	security-scan: semgrep-local
		@echo "Executou todas as varreduras de segurança locais"
