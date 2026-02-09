# Tomato AI Guidance System - Production App

Complete AI-powered tomato farming assistant with disease detection, yield prediction, and fertilizer recommendations.

## 🚀 Quick Start

### Option 1: Docker (Recommended - No npm needed!)

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Run:
   ```bash
   cd "d:\STUDY PROJECT\tomato-ai-project"
   docker-compose up --build
   ```
3. Access:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Backend Only

```bash
python -c "from backend.database import init_db; init_db()"
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
Then visit http://localhost:8000/docs to use the API directly.

## ✨ Features

### 🦠 Disease Detection
- Upload tomato leaf images
- AI analysis using CNN or Vision Transformer
- 8 disease categories with 92%+ accuracy
- Treatment recommendations

### 📊 Yield Prediction
- ML-based yield forecasting
- Considers season, weather, soil NPK, variety
- Personalized recommendations

### 🌱 Fertilizer Advice
- Soil health card analysis
- NPK recommendations
- pH correction guidance

## 🏗️ Architecture

### Backend (FastAPI)
- RESTful API with JWT authentication
- SQLAlchemy ORM with SQLite/PostgreSQL
- TensorFlow/Keras for ML models
- Automatic API documentation (Swagger)

### Frontend (React + Material-UI)
- Modern responsive design
- Protected routes with authentication
- Real-time predictions
- Mobile-friendly interface

### ML Models
- **CNN (MobileNetV2)** - Disease detection
- **ViT (Vision Transformer)** - Disease detection
- **RandomForest** - Yield prediction

## 📁 Project Structure

```
tomato-ai-project/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── models.py            # Database models
│   ├── auth.py              # JWT authentication
│   ├── ml_service.py        # ML inference
│   └── routers/
│       ├── auth.py          # Auth endpoints
│       ├── disease.py       # Disease API
│       └── yield_pred.py    # Yield API
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   └── package.json
├── models/
│   ├── disease_model.h5     # CNN model
│   ├── disease_vit_model.h5 # ViT model
│   └── yield_model.joblib   # Yield model
├── docker-compose.yml
└── DEPLOYMENT.md
```

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for:
- Docker (local/production)
- Railway (free hosting)
- Render (free hosting)
- AWS/GCP/Azure

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (interactive)
- **Backend Guide**: [BACKEND_QUICKSTART.md](BACKEND_QUICKSTART.md)
- **Frontend Guide**: [frontend/README.md](frontend/README.md)
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)

## 🔧 Development

### Backend
```bash
pip install -r backend/requirements.txt
python -m backend.database  # Initialize DB
uvicorn backend.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📝 License

MIT License - Free for educational and commercial use.

---

**Built with:**  Python | FastAPI | React | TensorFlow | Material-UI | Docker
