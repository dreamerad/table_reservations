#!/bin/bash
set -e

alembic revision --autogenerate -m "$1"

echo "Migration created successfully!"