#!/bin/bash

# Run tests with coverage
python -m pytest --cov=src --cov-report=term-missing --cov-report=html

# View the HTML coverage report with Brave browser
brave-browser "file://$(pwd)/coverage_html/index.html"