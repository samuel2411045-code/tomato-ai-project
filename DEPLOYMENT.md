# Tomato AI - Production Deployment Guide

## Prerequisites

- Docker Desktop (includes Docker and Docker Compose)
- Download from: https://www.docker.com/products/docker-desktop/

## Quick Start with Docker

### 1. Install Docker Desktop
Download and install Docker Desktop for Windows from the link above.

### 2. Build and Run

```bash
# Navigate to project directory
cd "d:\STUDY PROJECT\tomato-ai-project"

# Build and start all services
docker-compose up --build
```

This will:
- Build the FastAPI backend (Python)
- Build the React frontend (Node.js → static files)
- Start both services automatically
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

### 3. Stop Services

```bash
docker-compose down
```

## Alternative: Run Backend Only (No Docker/npm needed)

If you don't want to use Docker, you can run just the backend API:

```bash
# Initialize database
python -c "from backend.database import init_db; init_db()"

# Start backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Then access the API documentation at http://localhost:8000/docs

## Production Deployment

### Railway (Free Tier)
1. Push to GitHub
2. Connect Railway to your repo
3. Deploy automatically

### Render (Free Tier)
1. Push to GitHub
2. Create new Web Service on Render
3. Connect repo and deploy

### AWS/GCP/Azure
Use the Dockerfiles for containerized deployment to cloud platforms.

## Environment Variables

Create `.env` file:

```
DATABASE_URL=sqlite:///./tomato_ai.db
SECRET_KEY=your-super-secret-key-here
```

For production, use PostgreSQL:
```
DATABASE_URL=postgresql://user:password@host:port/dbname
```
