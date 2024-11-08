# PostgreSQL Dockerfile

This Dockerfile configures the PostgreSQL image for the Data-Infrastructure Challenge project.

## Features

- Based on the official PostgreSQL image.
- Includes custom configurations for the service.

## Environment Variables

- `POSTGRES_USER`: Database user.
- `POSTGRES_PASSWORD`: Database password.
- `POSTGRES_DB`: Database name.

## Usage

This Dockerfile is automatically used by docker-compose.yml in the project root.

## PostgreSQL Initialization Script

This `init.sql` script initializes the PostgreSQL database for the Data-Infrastructure Challenge project.

## Contents

- Creates schemas and tables needed for the project.
- Inserts initial data for testing.

This script is automatically executed by the PostgreSQL service.