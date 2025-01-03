# Development Guide

## Folder structure

```
homelife/
├── backend/         # Django backend
│   ├── manage.py
│   ├── backend/     # Django project folder
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   └── api/         # Django app for API
│       ├── models.py
│       ├── views.py
│       ├── serializers.py
│       ├── urls.py
├── frontend/        # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   ├── index.js
├── requirements.txt # Python dependencies
├── package.json     # Frontend dependencie
├── .env             # Environment variables
```

## Development environment

Mac is a pretty typical environment for developing and this project is largely developed using a mac.

### Installing postgres on mac

The homebrew install of mac works pretty well for development but there can often be problems along the way. Using Homebrew here is a quick guide of how the install went.

```bash
$ brew update
$ brew doctor
$ brew install postgresql@16
$ brew services start postgresql@16
$ echo 'export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"' >> ~/.zshrc
$ psql
```

If you get an error connecting to the tmp file it might be worth your time to uninstall everything and make sure there is no other postgres on your system. For example to remove postgres@14 would be something like:

```bash
$ brew remove --force postgresql
$ brew remove --force postgresql@14
$ rm -rf /usr/local/var/postgres/
$ rm -rf /usr/local/var/postgresql@14/
# for Apple Silicon might need
# rm -rf /opt/homebrew/var/postgres
# rm -rf /opt/homebrew/var/postgresql@14
```

### Tests

When writing new backend models, it is important to keep tests working.

### Adding Models to the Admin Portal

To add models to the Django admin portal, follow these steps:

1. Open `backend/api/admin.py`.
2. Import the models you want to add:
    ```python
    from .models import YourModel
    ```
3. Register the models with the admin site:
    ```python
    from django.contrib import admin
    admin.site.register(YourModel)
    ```

### Creating Data

To create data for your models, you can use the Django shell or create a script:

1. Open the Django shell:
    ```bash
    $ python manage.py shell
    ```
2. Create instances of your models:
    ```python
    from api.models import YourModel
    instance = YourModel(field1='value1', field2='value2')
    instance.save()
    ```

### Dumping Data to a Fixture

To dump data to a fixture, use the `dumpdata` management command:

1. Run the following command to dump data to a JSON file:
    ```bash
    $ python manage.py dumpdata api.YourModel --indent 4 > api/fixtures/yourmodel_data.json
    ```

### Writing a Test on the Fixture

To write a test using the fixture, follow these steps:

1. Create a test file `backend/api/tests/test_yourmodel.py`.
2. Load the fixture and write your test:
    ```python
    from django.test import TestCase
    from django.core.management import call_command
    from api.models import YourModel

    class YourModelTestCase(TestCase):
        fixtures = ['yourmodel_data.json']

        def setUp(self):
            call_command('loaddata', 'yourmodel_data.json')

        def test_yourmodel(self):
            instance = YourModel.objects.get(pk=1)
            self.assertEqual(instance.field1, 'value1')
    ```