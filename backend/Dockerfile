FROM golang:1.22.6 as migrate

RUN go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest

# Use a slimmer image to reduce size
FROM python:3.11-slim 

# Set environment variables
ENV FLASK_APP=app.py
# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/* 

COPY --from=migrate /go/bin/migrate /usr/local/bin/migrate

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "migrate -path ./migrations -database $DATABASE_URL up && flask run --host=0.0.0.0"]
