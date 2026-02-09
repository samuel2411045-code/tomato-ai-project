# Tomato AI Backend API - Quick Start

## Installation

```bash
# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib python-multipart pillow

# Note: TensorFlow and scikit-learn are already installed
```

## Initialize Database

```bash
python -c "from backend.database import init_db; init_db()"
```

## Run Server

```bash
# Development mode with auto-reload
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

**Authentication:**
- POST `/api/auth/signup` - Register new user
- POST `/api/auth/login` - Login and get token

**Disease Detection:**
- POST `/api/disease/predict` - Upload leaf image for disease detection
- GET `/api/disease/history` - Get prediction history

**Yield Prediction:**
- POST `/api/yield/predict` - Get yield forecast
- GET `/api/yield/history` - Get yield history

**Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Example Usage

### 1. Register
```bash
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"username":"farmer1","email":"farmer@example.com","password":"secure123","full_name":"John Farmer"}'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"farmer1","password":"secure123"}'
```

### 3. Predict Disease (use token from login)
```bash
curl -X POST "http://localhost:8000/api/disease/predict?model_type=CNN" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "image=@/path/to/leaf.jpg"
```
