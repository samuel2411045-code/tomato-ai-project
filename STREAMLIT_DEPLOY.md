# Streamlit Cloud Deployment Guide

## Prerequisites
- GitHub account
- Your code pushed to GitHub repository

## Step-by-Step Deployment

### 1. Prepare Your Repository
Make sure you have these files (already created for you):
- ✅ `app.py` (main Streamlit app)
- ✅ `requirements.txt` (Python dependencies)
- ✅ `packages.txt` (System dependencies for OCR)
- ✅ All your optimized model files in `models/` folder

### 2. Push to GitHub
If you haven't already:
1. Open **GitHub Desktop**
2. Make sure all files (especially `models/disease_model.h5` and `models/yield_model.joblib`) are committed
3. Click **"Push origin"** to upload to GitHub

### 3. Deploy on Streamlit Cloud

#### A. Sign In
1. Go to: https://share.streamlit.io/
2. Click **"Sign in"**
3. Use your GitHub account to sign in

#### B. Deploy New App
1. Click **"New app"** button
2. Fill in the form:
   - **Repository**: Select your `tomato-ai-project` repo
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (custom): Choose a unique name

3. Click **"Deploy!"**

#### C. Wait for Deployment
- Streamlit installs all dependencies from `requirements.txt`
- It will automatically set up the Tesseract OCR engine from `packages.txt`
- The app will start using your high-accuracy models (~81% disease detection).

### 4. Your App is Live! 🎉
Example: `https://your-tomato-app.streamlit.app`

---

## Your Optimized App Features

🍅 **High-Accuracy Leaf Detection**
- Uses **CNN (MobileNetV2)** with ~81% accuracy.
- Optimized for **Tomato Leaves** only to ensure reliability.
- Treatment recommendations for 8 disease types.

📊 **Enhanced Yield Prediction**
- **0.88 R² Score** model trained on 10,000 samples.
- Accurate forecasting based on NPK, weather, and season.

🌱 **Soil Health Integration**
- Soil health card OCR for automatic data entry.
- Personalized fertilizer logic.

---

**Ready to deploy?** Follow the steps above and your optimized app will be live and shared with the world!
