from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model for authentication and profile."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    phone = Column(String)
    role = Column(String, default="farmer")  # farmer, expert, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    farms = relationship("Farm", back_populates="owner")
    predictions = relationship("DiseasePrediction", back_populates="user")
    yield_forecasts = relationship("YieldForecast", back_populates="user")

class Farm(Base):
    """Farm profile with location data."""
    __tablename__ = "farms"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    location = Column(String)  # Address
    latitude = Column(Float)
    longitude = Column(Float)
    area_hectares = Column(Float)
    variety = Column(String)  # Desi, Hybrid, Cherry, Beefsteak
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="farms")
    soil_data = relationship("SoilData", back_populates="farm")

class SoilData(Base):
    """Soil health card records."""
    __tablename__ = "soil_data"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    ph = Column(Float)
    nitrogen = Column(Float)
    phosphorus = Column(Float)
    potassium = Column(Float)
    organic_carbon = Column(Float)
    ec = Column(Float)  # Electrical Conductivity
    test_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    farm = relationship("Farm", back_populates="soil_data")

class DiseasePrediction(Base):
    """Historical disease predictions."""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_path = Column(String)
    model_type = Column(String)  # CNN, ViT
    predicted_disease = Column(String)
    confidence = Column(Float)
    all_predictions = Column(JSON)  # Store all class probabilities
    treatment_advice = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="predictions")

class YieldForecast(Base):
    """Yield prediction history."""
    __tablename__ = "yield_forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    season = Column(String)  # Kharif, Rabi, Zayad
    temperature = Column(Float)
    rainfall = Column(Float)
    humidity = Column(Float)
    predicted_yield = Column(Float)
    prediction_type = Column(String)  # heuristic, ml
    input_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="yield_forecasts")

class WeatherCache(Base):
    """Cached weather API responses."""
    __tablename__ = "weather_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    weather_data = Column(JSON)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
