# Final Challenge: Complete Workflow (Build, Run, Push)

This lab completes the full workflow using a simple Python web app and PostgreSQL.

## Project Files

- `app.py`: Flask API (`/`, `/health`, `/visits`)
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container definition for app
- `docker-compose.yml`: App + database stack
- `.dockerignore`: Excludes unneeded files from build context

## 1) Create a Simple Web App

A Flask app is implemented with endpoints:

- `GET /` returns a welcome message
- `GET /health` returns app health
- `GET /visits` inserts and returns total visits from PostgreSQL

## 2) Write Dockerfile

The Dockerfile uses `python:3.12-slim`, installs dependencies, copies app code, and exposes port `5000`.

## 3) Build the Image with Proper Tags

From this folder:

```bash
docker build -t docker101/final-workflow-app:1.0.0 -t docker101/final-workflow-app:latest .
```

## 4) Run and Test the Container (Standalone)

Run app only:

```bash
docker run --rm -p 5000:5000 --name final-workflow-app docker101/final-workflow-app:1.0.0
```

Test in another terminal:

```bash
curl http://localhost:5000/
curl http://localhost:5000/health
```

Note: `/visits` requires PostgreSQL, so use Docker Compose for full testing.

## 5) Push to Docker Hub or GHCR

### Docker Hub

```bash
docker login
docker push docker101/final-workflow-app:1.0.0
docker push docker101/final-workflow-app:latest
```

### GHCR (example)

```bash
docker tag docker101/final-workflow-app:1.0.0 ghcr.io/<your-username>/final-workflow-app:1.0.0
docker tag docker101/final-workflow-app:latest ghcr.io/<your-username>/final-workflow-app:latest
echo <GITHUB_TOKEN> | docker login ghcr.io -u <your-username> --password-stdin
docker push ghcr.io/<your-username>/final-workflow-app:1.0.0
docker push ghcr.io/<your-username>/final-workflow-app:latest
```

## 6) Create Docker Compose (App + DB)

Start stack:

```bash
docker compose up -d --build
```

Check services:

```bash
docker compose ps
```

Test endpoints:

```bash
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/visits
curl http://localhost:5000/visits
```

View logs:

```bash
docker compose logs -f app
```

Stop stack:

```bash
docker compose down
```

Stop and remove volumes:

```bash
docker compose down -v
```

## 7) Documentation

This file serves as the challenge documentation and runbook.
