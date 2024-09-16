#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    SELECT 'CREATE DATABASE lac_fullstack_dev'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'lac_fullstack_dev')\gexec
    GRANT ALL PRIVILEGES ON DATABASE lac_fullstack_dev TO "$POSTGRES_USER";
EOSQL