# Operations Guide for Django Backend Tasks

## Table of Contents
1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Running the Server](#running-the-server)
4. [Database Migrations](#database-migrations)
5. [Running Tests](#running-tests)
6. [Common Tasks](#common-tasks)
7. [Troubleshooting](#troubleshooting)

## Introduction
This guide provides instructions for managing and operating the Django backend tasks for this repository.

## Setup
1. **Clone the repository:**
    ```bash
    git clone https://github.com/aterrel/homelife.git
    cd homelife
    ```

1. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

1. **Set up environment variables:**
    Create a `.env` file in the root directory and add the necessary environment variables.

1. **Create a database**
    Create a postgres database for the application to store data. For example see the script `/scripts/create-db.sh`
    ```bash
    ./scripts/create-db.sh
    ```

## Running the Server
To start the Django development server, run:
```bash
python manage.py runserver
```
The server will be accessible at `http://127.0.0.1:8000/`.

## Database Migrations
1. **Create new migrations:**
    ```bash
    python manage.py makemigrations
    ```

1. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

## Running Tests
To run the test suite, use:
```bash
python manage.py test
```

## Common Tasks
- **Create a superuser:**
  ```bash
  python manage.py createsuperuser
  ```

- **Collect static files:**
  ```bash
  python manage.py collectstatic
  ```

- **Open the Django shell:**
  ```bash
  python manage.py shell
  ```

## Troubleshooting
- **Server not starting:**
  Ensure all dependencies are installed and environment variables are correctly set.

- **Database issues:**
  Check if migrations are applied and the database is correctly configured.

For further assistance, refer to the [Django documentation](https://docs.djangoproject.com/).
