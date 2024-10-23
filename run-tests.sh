#!/bin/bash

# Ensure we're using the virtual environment's Python
VENV_PATH="./venv"
if [[ ! -d "${VENV_PATH}" ]]; then
    echo "Virtual environment not found at ${VENV_PATH}"
    exit 1
fi

# shellcheck disable=SC1091
source "${VENV_PATH}/bin/activate"

# Run tests with coverage
"${VENV_PATH}/bin/python" -m pytest -v \
    --cov=src \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-config=.coveragerc

# View the HTML coverage report with the default web browser
    brave-browser "file://$(pwd)/coverage_html/index.html"
