     psql postgres -c "CREATE DATABASE homelife_db;"
     psql postgres -c "CREATE USER homelife_user WITH PASSWORD 'homelife_password';"
     psql postgres -c "ALTER DATABASE homelife_db OWNER TO homelife_user;"
     psql postgres -c "ALTER USER homelife_user CREATEDB;"  # allow user to create databases for testing
     psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE homelife_db TO homelife_user;"
