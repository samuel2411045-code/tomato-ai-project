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
- ✅ All your model files in `models/` folder

### 2. Push to GitHub
If you haven't already:
1. Open **GitHub Desktop**
2. Make sure all files are committed
3. Click **"Push origin"** to upload to GitHub

### 3. Deploy on Streamlit Cloud

#### A. Sign In
1. Go to: https://share.streamlit.io/
2. Click **"Sign in"**
3. Use your GitHub account to sign in

#### B. Deploy New App
1. Click **"New app"** button
2. Fill in the form:
   - **Repository**: Select `tomato-ai-system` (or your repo name)
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (custom): Choose a name like `tomato-ai-assistant`

3. Click **"Deploy!"**

#### C. Wait for Deployment
- First deployment takes 5-10 minutes
- Streamlit installs all dependencies
- Uploads your ML models
- The app will automatically start

### 4. Your App is Live! 🎉

Your app will be available at:
```
https://YOUR_APP_NAME.streamlit.app
```

For example: `https://tomato-ai-assistant.streamlit.app`

**Share this URL with anyone!** They can use your app without installing anything.

---

## Features on Streamlit Cloud

✅ **Free Forever** for public apps
✅ **Auto-updates** when you push to GitHub
✅ **Automatic SSL** (HTTPS)
✅ **No server management**
✅ **Built-in analytics**

---

## Troubleshooting

### If deployment fails:

**1. Model Files Too Large**
If your models are >200MB total, you might hit limits. Solutions:
- Use Git LFS (Large File Storage)
- Host models on Hugging Face and download them in the app

**2. Memory Errors**
Streamlit Cloud has 1GB RAM limit. Your models should fit fine.

**3. Tesseract OCR Issues**
The `packages.txt` file installs Tesseract automatically. If it fails, check the deployment logs.

---

## After Deployment

### Update Your App
1. Make changes to your code locally
2. Commit changes in GitHub Desktop
3. Push to GitHub
4. **Streamlit auto-deploys** the new version!

### View Logs
- Click **"Manage app"** on Streamlit Cloud
- View logs to debug any issues

### Analytics
- See how many people use your app
- View usage statistics

---

## Alternative: Deploy as Private App

If you want to keep it private:
1. Make your GitHub repo private
2. Deploy as usual
3. Only people with the link can access it

---

## Your App Features (What Users Will See)

🍅 **Disease Detection**
- Upload tomato leaf images
- AI analysis with CNN or ViT
- Treatment recommendations

📊 **Yield Prediction**
- Weather-based forecasting
- Soil analysis integration
- Season recommendations

🌱 **Fertilizer Advice**
- Soil health card OCR
- NPK recommendations
- Bio-fertilizer suggestions

---

**Ready to deploy?** Follow the steps above and your app will be live in minutes!
