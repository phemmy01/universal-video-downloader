# Create deployment files for different hosting platforms

# 1. Create requirements.txt for all platforms
requirements_txt = '''flask==2.3.3
flask-cors==4.0.0
yt-dlp==2023.12.30
gunicorn==21.2.0
'''

with open('requirements.txt', 'w') as f:
    f.write(requirements_txt)

# 2. Create Procfile for Railway/Heroku deployment
procfile = '''web: gunicorn --bind 0.0.0.0:$PORT server:app
'''

with open('Procfile', 'w') as f:
    f.write(procfile)

# 3. Create render.yaml for Render deployment
render_yaml = '''services:
  - type: web
    name: video-downloader
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT server:app
    plan: free
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.16
'''

with open('render.yaml', 'w') as f:
    f.write(render_yaml)

# 4. Create railway.json for Railway deployment  
railway_json = '''{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT server:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}'''

with open('railway.json', 'w') as f:
    f.write(railway_json)

# 5. Create vercel.json for Vercel deployment
vercel_json = '''{
  "version": 2,
  "builds": [
    {
      "src": "server.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "server.py"
    }
  ]
}'''

with open('vercel.json', 'w') as f:
    f.write(vercel_json)

# 6. Create .gitignore
gitignore = '''__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Environment variables
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Downloads folder (temporary files)
downloads/*
!downloads/.gitkeep
'''

with open('.gitignore', 'w') as f:
    f.write(gitignore)

# 7. Create deployment guide
deployment_guide = '''# 🚀 Free Online Deployment Guide
## Deploy Your Video Downloader for Free

### 📋 Prerequisites
Make sure you have these files ready:
- server.py (your main application)
- requirements.txt 
- Procfile
- render.yaml
- railway.json
- vercel.json
- .gitignore

---

## 🎯 Method 1: Railway (Recommended - Easiest)

### ✅ Pros:
- Completely FREE (includes database)
- Very easy setup (2 clicks)
- Good for video processing
- No credit card required
- 500 hours/month free

### 📝 Steps:
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Railway automatically detects Flask and deploys
6. Get your live URL: `https://yourapp.up.railway.app`

### 🔧 Setup:
```bash
# Upload your files to GitHub first
git init
git add .
git commit -m "Video downloader app"
git remote add origin https://github.com/yourusername/video-downloader
git push -u origin main
```

---

## 🎯 Method 2: Render (Great Performance)

### ✅ Pros:
- FREE tier available
- Good performance
- Automatic SSL
- Great for Python apps

### 📝 Steps:
1. Go to https://render.com
2. Connect GitHub account
3. Select "New Web Service"
4. Choose your repository
5. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT server:app`
6. Deploy and get URL

---

## 🎯 Method 3: PythonAnywhere (Python-Focused)

### ✅ Pros:
- Made specifically for Python
- FREE plan available
- Easy Python setup
- Good for beginners

### 📝 Steps:
1. Go to https://www.pythonanywhere.com
2. Create free account
3. Upload files via their file manager
4. Set up web app:
   - Go to "Web" tab
   - Add new web app
   - Choose Flask
   - Point to your server.py
5. Install packages in console:
   ```bash
   pip3.10 install --user flask flask-cors yt-dlp
   ```

---

## 🎯 Method 4: Glitch (Collaborative)

### ✅ Pros:
- Completely FREE
- Live code editing
- Community features
- No setup required

### 📝 Steps:
1. Go to https://glitch.com
2. Click "New Project" → "Import from GitHub"
3. Paste your GitHub repo URL
4. Glitch automatically runs your Flask app
5. Get instant URL

---

## ⚡ Quick Deploy Commands

### For Railway:
```bash
# Install Railway CLI (optional)
npm install -g @railway/cli
railway login
railway deploy
```

### For Render:
```bash
# Just push to GitHub, Render auto-deploys
git push origin main
```

---

## 🔒 Important Notes

### ⚠️ Legal Considerations:
- Add terms of service about respecting copyright
- Consider rate limiting to prevent abuse
- Monitor usage to stay within free limits

### 🛡️ Security:
- Never include API keys in public repos
- Use environment variables for sensitive data
- Consider adding user authentication

### 📊 Free Tier Limits:
- **Railway:** 500 hours/month, 8GB RAM
- **Render:** 750 hours/month, 512MB RAM  
- **PythonAnywhere:** Always-on free app
- **Glitch:** Sleeps after 5 minutes of inactivity

---

## 🌍 Your Live URLs

After deployment, your video downloader will be available at:
- Railway: `https://video-downloader-production.up.railway.app`
- Render: `https://your-app-name.onrender.com`
- PythonAnywhere: `https://yourusername.pythonanywhere.com`
- Glitch: `https://your-project.glitch.me`

---

## 🚀 Recommended Deployment Order:

1. **Railway** (easiest, best performance)
2. **Render** (good alternative)
3. **PythonAnywhere** (Python-specific)
4. **Glitch** (if others fail)

Choose Railway for the best experience!
'''

with open('DEPLOYMENT_GUIDE.md', 'w') as f:
    f.write(deployment_guide)

print("✅ Created all deployment files:")
print("• requirements.txt - Package dependencies")
print("• Procfile - For Railway/Heroku") 
print("• render.yaml - For Render hosting")
print("• railway.json - For Railway hosting")
print("• vercel.json - For Vercel hosting")
print("• .gitignore - Git ignore file")
print("• DEPLOYMENT_GUIDE.md - Complete deployment instructions")
print("\n🎯 RECOMMENDED: Use Railway (easiest and free)")