#!/bin/bash
set -e

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the project root directory
cd "$DIR/../backend"

# Activate virtual environment if it exists
if [ -d "../venv" ]; then
    source ../venv/bin/activate
fi

# First flush the database
echo "Flushing existing data..."
python manage.py flush --no-input

# Load all fixtures
echo "Loading fixtures..."
python manage.py loaddata api/fixtures/test_users.json
# Add more fixtures here as needed

# Deactivate virtual environment if it was activated
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi
