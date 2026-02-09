from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any
import numpy as np
from PIL import Image
import io
from ..database import get_db
from ..models import User, DiseasePrediction
from ..auth import get_current_user
from ..ml_service import ml_service

router = APIRouter()

# Request/Response schemas
class DiseaseResponse(BaseModel):
    disease: str
    confidence: float
    all_predictions: Dict[str, float]
    model_used: str
    treatment_advice: str

# Treatment advice mapping
TREATMENT_ADVICE = {
    "Healthy": "Your tomato plant looks healthy! Continue regular care and monitoring.",
    "Early_blight": "Apply fungicides like chlorothalonil or mancozeb. Remove infected leaves. Ensure proper spacing for air circulation.",
    "Late_blight": "Apply copper-based fungicides immediately. Remove and destroy infected plants. Avoid overhead irrigation.",
    "Leaf Miner": "Use neem oil spray. Remove affected leaves. Consider beneficial insects like parasitic wasps.",
    "Magnesium Deficiency": "Apply Epsom salt (1 tbsp per gallon of water). Add dolomitic lime to soil. Foliar spray with magnesium sulfate.",
    "Nitrogen Deficiency": "Apply nitrogen-rich fertilizer (urea 46% N). Use organic options like compost or blood meal. Side-dress with ammonium nitrate.",
    "Pottassium Deficiency": "Apply potash fertilizer (muriate of potash). Use wood ash. Add organic matter like banana peels.",
    "Spotted Wilt Virus": "No cure available. Remove and destroy infected plants immediately. Control thrips vectors with insecticides. Use resistant varieties."
}

@router.post("/predict", response_model=DiseaseResponse)
async def predict_disease(
    image: UploadFile = File(...),
    model_type: str = "CNN",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Detect disease from tomato leaf image.
    
    - **image**: Leaf image file (JPG, PNG)
    - **model_type**: "CNN" or "ViT"
    """
    try:
        # Validate model type
        if model_type not in ["CNN", "ViT"]:
            raise HTTPException(status_code=400, detail="Invalid model type. Use 'CNN' or 'ViT'")
        
        # Read and preprocess image
        contents = await image.read()
        img = Image.open(io.BytesIO(contents)).convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        
        # Predict
        result = ml_service.predict_disease(img_array, model_type)
        
        # Get treatment advice
        disease = result["disease"]
        treatment = TREATMENT_ADVICE.get(disease, "Consult an agricultural expert for specific treatment.")
        
        # Save prediction to database
        prediction = DiseasePrediction(
            user_id=current_user.id,
            model_type=model_type,
            predicted_disease=disease,
            confidence=result["confidence"],
            all_predictions=result["all_predictions"],
            treatment_advice=treatment
        )
        db.add(prediction)
        db.commit()
        
        return {
            **result,
            "treatment_advice": treatment
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/history")
async def get_prediction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get user's disease prediction history."""
    predictions = db.query(DiseasePrediction)\
        .filter(DiseasePrediction.user_id == current_user.id)\
        .order_by(DiseasePrediction.created_at.desc())\
        .limit(limit)\
        .all()
    
    return [
        {
            "id": p.id,
            "disease": p.predicted_disease,
            "confidence": p.confidence,
            "model_type": p.model_type,
            "date": p.created_at.isoformat()
        }
        for p in predictions
    ]
