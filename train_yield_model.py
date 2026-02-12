import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

def train_yield_model():
    print("--- Starting Yield Model Training (High Accuracy) ---")
    
    # 1. Generate High-Volume Synthetic Data (10,000 samples)
    np.random.seed(42)
    n_samples = 10000  # Increased from 1,000 for better generalization
    
    print(f"Generating {n_samples} synthetic samples...")

    # Season encoding: Kharif=0, Rabi=1, Zayad=2
    season = np.random.choice([0, 1, 2], n_samples)

    # Weather features (wider ranges to cover extremes)
    temperature = np.random.uniform(15, 40, n_samples)  # °C
    rainfall = np.random.uniform(0, 400, n_samples)     # mm
    humidity = np.random.uniform(30, 95, n_samples)     # %

    # Soil features
    nitrogen = np.random.uniform(100, 400, n_samples)   # kg/ha
    phosphorus = np.random.uniform(20, 120, n_samples)  # kg/ha
    potassium = np.random.uniform(80, 300, n_samples)   # kg/ha
    ph = np.random.uniform(5.0, 8.5, n_samples)
    organic_carbon = np.random.uniform(0.2, 1.5, n_samples)  # %

    # Variety encoding: Desi=0, Hybrid=1, Cherry=2, Beefsteak=3
    variety = np.random.choice([0, 1, 2, 3], n_samples)

    # Base yield logic (Simulation of ground truth)
    base_yield = 15.0

    # Season impact
    season_impact = np.where(season == 0, 1.2,      # Kharif (best)
                    np.where(season == 1, 1.0,      # Rabi
                             0.8))                   # Zayad (worst)

    # Temperature impact (optimal 20-28°C)
    temp_impact = 1.0 - 0.02 * np.abs(temperature - 24)
    temp_impact = np.clip(temp_impact, 0.5, 1.0) # Prevent negative or too low

    # Rainfall impact (optimal 150-200mm)
    rain_impact = 1.0 - 0.003 * np.abs(rainfall - 175)
    rain_impact = np.clip(rain_impact, 0.6, 1.0)

    # NPK impact (Sigmoid-like curve simulation)
    npk_impact = (nitrogen / 250) * 0.4 + (phosphorus / 70) * 0.3 + (potassium / 175) * 0.3
    npk_impact = np.clip(npk_impact, 0.5, 1.5)

    # pH impact (optimal 6.0-7.0)
    ph_impact = 1.0 - 0.1 * np.abs(ph - 6.5)
    ph_impact = np.clip(ph_impact, 0.7, 1.0)

    # Variety impact
    variety_impact = np.where(variety == 0, 0.8,    # Desi
                     np.where(variety == 1, 1.2,    # Hybrid (best)
                     np.where(variety == 2, 0.9,    # Cherry
                              1.1)))                 # Beefsteak

    # Calculate yield with realistic noise
    yield_val = (base_yield * season_impact * temp_impact * rain_impact * 
                  npk_impact * ph_impact * variety_impact * 
                  np.random.uniform(0.95, 1.05, n_samples)) # Reduced noise for clearer signal

    # Clip to realistic range (5-25 tons/ha)
    yield_val = np.clip(yield_val, 5, 30)

    # Create DataFrame
    df = pd.DataFrame({
        'season': season,
        'temperature': temperature,
        'rainfall': rainfall,
        'humidity': humidity,
        'nitrogen': nitrogen,
        'phosphorus': phosphorus,
        'potassium': potassium,
        'ph': ph,
        'organic_carbon': organic_carbon,
        'variety': variety,
        'yield': yield_val
    })

    # 2. Data Splitting
    X = df.drop('yield', axis=1)
    y = df['yield']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Model Training (Optimized Hyperparameters)
    print("\nTraining RandomForest (Optimized)...")
    model = RandomForestRegressor(
        n_estimators=300,       # Increased trees
        max_depth=15,           # Deeper trees
        min_samples_split=4,
        min_samples_leaf=2,
        max_features='sqrt',    # Standard for regression
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)

    # 4. Evaluation
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Cross-validation for robustness check
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
    
    print(f"\nModel Performance:")
    print(f"MAE: {mae:.2f} tons/ha")
    print(f"R² Score (Test): {r2:.4f}")
    print(f"R² Score (CV Mean): {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

    if r2 > 0.9:
        print("[SUCCESS] Excellent accuracy achieved (>0.9 R2)")
    else:
        print("[INFO] Accuracy is decent but could be improved.")

    # 5. Save Model
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    model_path = os.path.join(MODELS_DIR, "yield_model.joblib")
    joblib.dump(model, model_path)
    print(f"\nModel saved to: {model_path}")

if __name__ == "__main__":
    train_yield_model()
