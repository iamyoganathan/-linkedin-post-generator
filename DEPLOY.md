# 🚀 Deployment Guide

Quick guide to deploy your LinkedIn Post Generator.

---

## Option 1: Streamlit Cloud (Recommended - FREE)

### Step-by-Step:

1. **Prepare Your Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Get Groq API Key**
   - Visit: https://console.groq.com
   - Sign up (free)
   - Create API key
   - Copy it (starts with `gsk_`)

3. **Deploy on Streamlit**
   - Go to: https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Repository: Select your repo
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Advanced settings"
   - Add secrets:
     ```
     GROQ_API_KEY = "gsk_your_actual_key_here"
     ```
   - Click "Deploy"

4. **Done!**
   - Your app will be live at: `https://your-app-name.streamlit.app`
   - Takes 2-3 minutes to deploy

---

## Option 2: Docker

### Build and Run:

```bash
# Build image
docker build -t linkedin-post-generator .

# Run container
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_api_key \
  linkedin-post-generator
```

Access at: http://localhost:8501

---

## Option 3: Heroku

### Deploy Steps:

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variable
heroku config:set GROQ_API_KEY=your_key

# Deploy
git push heroku main
```

---

## Option 4: Local Server

### Quick Start:

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_key" > .env

# Run
streamlit run app.py
```

---

## 🔒 Security Checklist

Before deploying:

- [ ] Never commit `.env` file
- [ ] Use secrets management
- [ ] Update `.gitignore`
- [ ] Rotate API keys periodically
- [ ] Use environment variables

---

## 🧪 Test Your Deployment

1. Visit your deployed URL
2. Enter a test topic
3. Generate a post
4. Verify all features work

---

## 📞 Need Help?

- Check application logs
- Verify API key is correct
- Ensure dependencies are installed
- Check Streamlit documentation

---

**Your app is ready to deploy! 🎉**
