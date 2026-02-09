from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..models import User, YieldForecast
from ..auth import get_current_user
from ..ml_service import ml_service

router = APIRouter()

# Request/Response schemas
class YieldPredictionRequest(BaseModel):
    season: str  # "Kharif", "Rabi", "Zayad"
    temperature: float  # °C
    rainfall: float  # mm
    humidity: float  # %
    nitrogen: float  # kg/ha
    phosphorus: float  # kg/ha
    potassium: float  # kg/ha
    ph: float
    organic_carbon: float  # %
    variety: str  # "Desi", "Hybrid", "Cherry", "Beefsteak"

class YieldResponse(BaseModel):
    predicted_yield: float
    prediction_type: str
    recommendations: list[str]

# Mappings
SEASON_MAP = {"Kharif": 0, "Rabi": 1, "Zayad": 2}
VARIETY_MAP = {"Desi": 0, "Hybrid": 1, "Cherry": 2, "Beefsteak": 3}

@router.post("/predict", response_model=YieldResponse)
async def predict_yield(
    data: YieldPredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Predict tomato yield based on environmental and soil factors.
    
    Returns predicted yield in tons/hectare with recommendations.
    """
    try:
        # Convert categorical to numerical
        season_num = SEASON_MAP.get(data.season, 0)
        variety_num = VARIETY_MAP.get(data.variety, 0)
        
        # Predict
        yield_pred = ml_service.predict_yield(
            season=season_num,
            temperature=data.temperature,
            rainfall=data.rainfall,
            humidity=data.humidity,
            nitrogen=data.nitrogen,
            phosphorus=data.phosphorus,
            potassium=data.potassium,
            ph=data.ph,
            organic_carbon=data.organic_carbon,
            variety=variety_num
        )
        
        # Determine prediction type
        prediction_type = "ml" if 'yield' in ml_service.models else "heuristic"
        
        # Generate recommendations
        recommendations = []
        
        if data.temperature < 20:
            recommendations.append("⚠️ Temperature is low. Consider using mulching or row covers.")
        elif data.temperature > 30:
            recommendations.append("⚠️ Temperature is high. Ensure adequate irrigation and shade.")
        
        if data.rainfall < 100:
            recommendations.append("💧 Low rainfall. Increase irrigation frequency.")
        elif data.rainfall > 250:
            recommendations.append("💧 High rainfall. Ensure proper drainage to avoid waterlogging.")
        
        if data.nitrogen < 200:
            recommendations.append("🌱 Nitrogen is low. Apply urea or compost.")
        if data.phosphorus < 50:
            recommendations.append("🌱 Phosphorus is low. Apply DAP fertilizer.")
        if data.potassium < 150:
            recommendations.append("🌱 Potassium is low. Apply muriate of potash.")
        
        if data.ph < 6.0:
            recommendations.append("⚗️ Soil is acidic. Apply lime to raise pH.")
        elif data.ph > 7.5:
            recommendations.append("⚗️ Soil is alkaline. Add sulfur or organic matter.")
        
        if yield_pred < 10:
            recommendations.append("📉 Yield is predicted to be low. Review all factors and consult an expert.")
        elif yield_pred > 18:
            recommendations.append("📈 Excellent yield expected! Maintain current practices.")
        
        # Save to database
        forecast = YieldForecast(
            user_id=current_user.id,
            season=data.season,
            temperature=data.temperature,
            rainfall=data.rainfall,
            humidity=data.humidity,
            predicted_yield=yield_pred,
            prediction_type=prediction_type,
            input_data=data.dict()
        )
        db.add(forecast)
        db.commit()
        
        return {
            "predicted_yield": round(yield_pred, 2),
            "prediction_type": prediction_type,
            "recommendations": recommendations if recommendations else ["✅ All parameters are optimal!"]
        }
    
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/history")
async def get_yield_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get user's yield prediction history."""
    forecasts = db.query(YieldForecast)\
        .filter(YieldForecast.user_id == current_user.id)\
        .order_by(YieldForecast.created_at.desc())\
        .limit(limit)\
        .all()
    
    return [
        {
            "id": f.id,
            "season": f.season,
            "predicted_yield": f.predicted_yield,
            "prediction_type": f.prediction_type,
            "date": f.created_at.isoformat()
        }
        for f in forecasts
    ]
