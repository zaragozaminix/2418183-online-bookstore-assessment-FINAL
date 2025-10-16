#!/bin/sh
set -ex

# Bypassing discovery by explicitly naming the test files
PYTHONPATH=. python -m pytest tests/test_models.py tests/test_app.py