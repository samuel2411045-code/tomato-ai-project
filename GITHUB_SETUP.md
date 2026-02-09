# Push to GitHub - Setup Guide

Git is not installed on your system. Here are two options to push your project to GitHub:

## Option 1: GitHub Desktop (Easiest - No Commands)

### Step 1: Install GitHub Desktop
1. Download from: https://desktop.github.com/
2. Install and sign in with your GitHub account

### Step 2: Add Repository
1. Click **"Add"** → **"Add Existing Repository"**
2. Choose: `d:\STUDY PROJECT\tomato-ai-project`
3. Click **"Create Repository"**

### Step 3: Make Initial Commit
1. You'll see all your files listed
2. Add commit message: `Initial commit: Tomato AI Production App`
3. Click **"Commit to main"**

### Step 4: Publish to GitHub
1. Click **"Publish repository"**
2. Choose repository name: `tomato-ai-system`
3. Add description: *AI-powered tomato farming assistant with disease detection and yield prediction*
4. Choose **Public** or **Private**
5. Click **"Publish repository"**

✅ Done! Your repo is now on GitHub.

---

## Option 2: Git Command Line

### Step 1: Install Git
Download from: https://git-scm.com/download/win

### Step 2: Initialize and Commit
```bash
cd "d:\STUDY PROJECT\tomato-ai-project"
git init
git add .
git commit -m "Initial commit: Tomato AI Production App"
```

### Step 3: Create GitHub Repo
1. Go to https://github.com/new
2. Repository name: `tomato-ai-system`
3. Description: *AI-powered tomato farming assistant*
4. Click **"Create repository"**

### Step 4: Push to GitHub
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/tomato-ai-system.git
git branch -M main
git push -u origin main
```

---

## ⚠️ Important Notes

### Model Files
Your ML models are **large** (20MB total):
- `disease_model.h5` - 11.4 MB
- `disease_vit_model.h5` - 6.2 MB
- `yield_model.joblib` - 2.4 MB

**Options:**
1. **Include them** (GitHub allows files up to 100MB)
2. **Use Git LFS** (Large File Storage)
3. **Exclude them** - Uncomment these lines in `.gitignore`:
   ```
   # models/*.h5
   # models/*.joblib
   ```

### Files Already Excluded
The `.gitignore` I created excludes:
- `data/` folder (training images)
- `archive.zip` (dataset)
- `*.db` files (database)
- `node_modules/` (npm packages)
- `debug_vit.py` (debug file)

---

## After Pushing to GitHub

### Deploy for Free:

**Railway:**
1. Go to https://railway.app/
2. Click **"Start a New Project"** → **"Deploy from GitHub repo"**
3. Select your repo
4. Railway auto-detects Docker and deploys!

**Render:**
1. Go to https://render.com/
2. Click **"New"** → **"Web Service"**
3. Connect GitHub repo
4. Render builds and deploys

Both platforms have free tiers perfect for this project!

---

## Recommended: GitHub Desktop

For the easiest experience, I recommend **GitHub Desktop**. It's visual, simple, and requires no command-line knowledge.
