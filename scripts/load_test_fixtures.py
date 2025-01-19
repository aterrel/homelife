#!/usr/bin/env python3
import os
import sys
import django
from pathlib import Path

def setup_django():
    # Add the project directory to the Python path
    project_root = Path(__file__).resolve().parent.parent
    sys.path.append(str(project_root / 'backend'))
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()

def load_fixtures():
    from django.core.management import call_command
    from django.contrib.auth.models import User
    from api.models import Event, Recipe
    
    # Get project root
    project_root = Path(__file__).resolve().parent.parent
    
    # Clear existing data
    print("Clearing existing data...")
    User.objects.all().delete()
    Event.objects.all().delete()
    Recipe.objects.all().delete()
    
    # List of fixtures to load
    fixtures = [
        str(project_root / 'backend' / 'api' / 'fixtures' / 'test_users.json'),
        # Add more fixtures here as they are created
    ]
    
    # Load each fixture
    for fixture in fixtures:
        print(f"Loading fixture: {fixture}")
        try:
            call_command('loaddata', fixture)
        except Exception as e:
            print(f"Error loading fixture {fixture}: {e}")
            return False
    
    # Verify data was loaded
    user_count = User.objects.count()
    print(f"\nFixtures loaded successfully!")
    print(f"Users created: {user_count}")
    
    return True

def main():
    print("Setting up Django environment...")
    setup_django()
    
    print("\nStarting fixture loading process...")
    success = load_fixtures()
    
    if success:
        print("\nAll fixtures loaded successfully!")
        sys.exit(0)
    else:
        print("\nError loading fixtures!")
        sys.exit(1)

if __name__ == '__main__':
    main()
