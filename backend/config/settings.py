import os

# Use environment variables or fallback to default values
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/lac_fullstack_dev?sslmode=disable')
