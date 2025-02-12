#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Go to the project root directory (one level up from scripts)
cd "$SCRIPT_DIR/../backend"

# Flush the database
echo "Flushing the database..."
python manage.py flush --no-input

# Load all fixtures
echo "Loading fixtures..."
echo "loading test users..."
python manage.py loaddata api/fixtures/test_users.json
echo "loading categories..."
python manage.py loaddata api/fixtures/category_data.json
echo "loading ingredients..."
python manage.py loaddata api/fixtures/ingredient_data.json
echo "loading recipes..."
python manage.py loaddata api/fixtures/recipe_data.json
echo "loading recipeingredients..."
python manage.py loaddata api/fixtures/recipeingredient_data.json
#echo "loading events..."
#python manage.py loaddata api/fixtures/event_data.json


# Create test users with proper passwords
echo "Creating test users..."
python manage.py shell << EOF
from django.contrib.auth.models import User
# Update testuser1
user = User.objects.get(username='testuser1')
user.set_password('testpass123')
user.save()
# Update adminuser
admin = User.objects.get(username='adminuser')
admin.set_password('testpass123')
admin.save()
EOF

echo "Fixtures loaded successfully!"
