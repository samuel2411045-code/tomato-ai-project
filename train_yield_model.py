import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

# Generate synthetic training data for tomato yield prediction
np.random.seed(42)

n_samples = 1000

# Season encoding: Kharif=0, Rabi=1, Zayad=2
season = np.random.choice([0, 1, 2], n_samples)

# Weather features
temperature = np.random.uniform(18, 35, n_samples)  # °C
rainfall = np.random.uniform(50, 300, n_samples)    # mm
humidity = np.random.uniform(60, 90, n_samples)     # %

# Soil features
nitrogen = np.random.uniform(150, 350, n_samples)   # kg/ha
phosphorus = np.random.uniform(40, 100, n_samples)  # kg/ha
potassium = np.random.uniform(100, 250, n_samples)  # kg/ha
ph = np.random.uniform(5.5, 7.5, n_samples)
organic_carbon = np.random.uniform(0.3, 1.2, n_samples)  # %

# Variety encoding: Desi=0, Hybrid=1, Cherry=2, Beefsteak=3
variety = np.random.choice([0, 1, 2, 3], n_samples)

# Create yield based on realistic patterns
base_yield = 15.0

# Season impact
season_impact = np.where(season == 0, 1.2,      # Kharif (best)
                np.where(season == 1, 1.0,      # Rabi
                         0.8))                   # Zayad (worst)

# Temperature impact (optimal 20-28°C)
temp_impact = 1.0 - 0.02 * np.abs(temperature - 24)

# Rainfall impact (optimal 150-200mm)
rain_impact = 1.0 - 0.003 * np.abs(rainfall - 175)

# NPK impact
npk_impact = (nitrogen / 250) * 0.4 + (phosphorus / 70) * 0.3 + (potassium / 175) * 0.3

# pH impact (optimal 6.0-7.0)
ph_impact = 1.0 - 0.1 * np.abs(ph - 6.5)

# Variety impact
variety_impact = np.where(variety == 0, 0.8,    # Desi
                 np.where(variety == 1, 1.2,    # Hybrid (best)
                 np.where(variety == 2, 0.9,    # Cherry
                          1.1)))                 # Beefsteak

# Calculate yield with noise
yield_tons = (base_yield * season_impact * temp_impact * rain_impact * 
              npk_impact * ph_impact * variety_impact * 
              np.random.uniform(0.9, 1.1, n_samples))

# Clip to realistic range (5-25 tons/ha)
yield_tons = np.clip(yield_tons, 5, 25)

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
    'yield': yield_tons
})

print("Dataset created:")
print(f"Total samples: {len(df)}")
print(f"\nYield statistics:")
print(df['yield'].describe())

# Split data
X = df.drop('yield', axis=1)
y = df['yield']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train RandomForest model
print("\nTraining RandomForest model...")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nModel Performance:")
print(f"MAE: {mae:.2f} tons/ha")
print(f"R² Score: {r2:.3f}")

# Save model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

model_path = os.path.join(MODELS_DIR, "yield_model.joblib")
joblib.dump(model, model_path)
print(f"\nModel saved to: {model_path}")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
print(feature_importance)
