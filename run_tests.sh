#!/bin/bash
# Test runner script for the High School Management System

echo "Running tests for High School Management System API..."
echo "=================================================="

# Run tests with coverage
python -m pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

echo ""
echo "Test run complete!"
echo "HTML coverage report generated in htmlcov/index.html"