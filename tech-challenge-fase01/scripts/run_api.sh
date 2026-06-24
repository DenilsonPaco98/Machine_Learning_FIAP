#!/bin/bash
# Script to run the FastAPI server

set -e

echo "Starting Churn Prediction API..."
python -m uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
