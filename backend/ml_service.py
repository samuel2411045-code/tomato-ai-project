import os
import numpy as np
from tensorflow import keras
import joblib
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)

# Model paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

class MLService:
    """ML model service for disease detection and yield prediction."""
    
    def __init__(self):
        self.models = {}
        self.class_names = [
            "Early_blight", "Healthy", "Late_blight", "Leaf Miner",
            "Magnesium Deficiency", "Nitrogen Deficiency",
            "Pottassium Deficiency", "Spotted Wilt Virus"
        ]
    
    def load_models(self):
        """Load all ML models."""
        try:
            # Load CNN disease model
            cnn_path = os.path.join(MODELS_DIR, "disease_model.h5")
            if os.path.exists(cnn_path):
                self.models['disease_cnn'] = keras.models.load_model(cnn_path)
                logger.info("Loaded CNN disease model")
            

            
            # Load yield model
            yield_path = os.path.join(MODELS_DIR, "yield_model.joblib")
            if os.path.exists(yield_path):
                self.models['yield'] = joblib.load(yield_path)
                logger.info("Loaded yield prediction model")
            
            return self.models
        
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    def predict_disease(
        self,
        image: np.ndarray,
    ) -> Dict[str, Any]:
        """
        Predict disease from tomato leaf image.
        
        Args:
            image: Preprocessed leaf image array (224, 224, 3)
        
        Returns:
            Dictionary with prediction results
        """
        try:
            if 'disease_cnn' not in self.models:
                raise ValueError("Disease model not loaded")
            
            model = self.models['disease_cnn']
            
            # Ensure correct shape
            if len(image.shape) == 3:
                image = np.expand_dims(image, axis=0)
            
            # Predict
            predictions = model.predict(image, verbose=0)[0]
            
            # Get top prediction
            top_idx = np.argmax(predictions)
            confidence = float(predictions[top_idx])
            disease = self.class_names[top_idx]
            
            # All predictions
            all_preds = {
                self.class_names[i]: float(predictions[i])
                for i in range(len(self.class_names))
            }
            
            return {
                "disease": disease,
                "confidence": confidence,
                "all_predictions": all_preds,
                "model_used": "CNN"
            }
        
        except Exception as e:
            logger.error(f"Error in disease prediction: {e}")
            raise
    
    def predict_yield(
        self,
        season: int,
        temperature: float,
        rainfall: float,
        humidity: float,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        ph: float,
        organic_carbon: float,
        variety: int
    ) -> float:
        """
        Predict tomato yield.
        
        Args:
            All input features for the yield model
        
        Returns:
            Predicted yield in tons/hectare
        """
        try:
            if 'yield' not in self.models:
                # Fallback to heuristic
                return self._heuristic_yield(
                    season, temperature, rainfall, nitrogen, phosphorus, potassium, ph
                )
            
            model = self.models['yield']
            
            # Prepare features
            features = np.array([[
                season, temperature, rainfall, humidity,
                nitrogen, phosphorus, potassium, ph, organic_carbon, variety
            ]])
            
            # Predict
            yield_pred = model.predict(features)[0]
            
            return float(yield_pred)
        
        except Exception as e:
            logger.error(f"Error in yield prediction: {e}")
            raise
    
    def _heuristic_yield(
        self,
        season: int,
        temperature: float,
        rainfall: float,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        ph: float
    ) -> float:
        """Fallback heuristic yield calculation."""
        base_yield = 15.0
        
        # Season impact
        season_impact = [1.2, 1.0, 0.8][season]
        
        # Temperature impact (optimal 20-28°C)
        temp_impact = 1.0 - 0.02 * abs(temperature - 24)
        
        # Rainfall impact (optimal 150-200mm)
        rain_impact = 1.0 - 0.003 * abs(rainfall - 175)
        
        # NPK impact
        npk_impact = (nitrogen / 250) * 0.4 + (phosphorus / 70) * 0.3 + (potassium / 175) * 0.3
        
        # pH impact (optimal 6.0-7.0)
        ph_impact = 1.0 - 0.1 * abs(ph - 6.5)
        
        yield_tons = base_yield * season_impact * temp_impact * rain_impact * npk_impact * ph_impact
        
        return max(5.0, min(25.0, yield_tons))

def load_models() -> Dict[str, Any]:
    """Load all ML models at startup."""
    service = MLService()
    return service.load_models()

# Global service instance
ml_service = MLService()
