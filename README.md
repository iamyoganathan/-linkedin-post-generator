# 📱 LinkedIn Post Generator

An AI-powered web application to generate engaging LinkedIn posts using Groq API and Streamlit.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-API-orange)](https://groq.com)

---

## ✨ Features

- **🤖 AI-Powered Generation**: Create professional LinkedIn posts in seconds
- **🎨 Multiple Tones**: Professional, Casual, Motivational, Educational, Storytelling, Thought-Leadership
- **📏 Length Control**: Short, Medium, or Long posts
- **#️⃣ Smart Hashtags**: Auto-generate relevant hashtags
- **🔄 Variations**: Generate 3 different versions
- **✨ Refinement**: Make posts shorter, longer, or more professional
- **📈 Engagement Predictor**: AI-powered engagement scoring
- **💾 Draft Management**: Save and organize your posts
- **📊 Analytics**: Track your usage and statistics

---

## 🚀 Quick Deploy to Streamlit Cloud (FREE)

### Step 1: Get Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up (takes 2 minutes, FREE forever)
3. Create API key
4. Copy the key (starts with `gsk_`)

### Step 2: Deploy

1. **Fork this repository** on GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"**
4. Select your forked repository
5. Set main file: `app.py`
6. Click **Advanced settings** → **Secrets**
7. Add:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_key_here"
   ```
8. Click **"Deploy"**

**Your app will be live in 2 minutes!** 🎉

URL: `https://your-app-name.streamlit.app`

---

## 💻 Local Development

```bash
# Clone repository
git clone <your-repo-url>
cd linkedin-post-generator

# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

# Run
streamlit run app.py
```

---

## 📱 How to Use

1. **Enter Topic**: Type what you want to write about
2. **Choose Tone**: Select from 6 tones
3. **Select Length**: Short, Medium, or Long
4. **Generate**: Click "🚀 Generate Post"
5. **Refine** (optional): Make it shorter, longer, etc.
6. **Copy**: Use on LinkedIn!

###Advanced Features

- 🔄 Generate 3 variations at once
- 🎣 Get attention-grabbing hooks
- 📈 Check engagement score
- 💾 Save drafts
- 📊 View analytics

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.9+
- **AI**: Groq API (Llama 3.3 70B)
- **Database**: SQLite
- **Charts**: Plotly

---

## ⚙️ Configuration

### For Streamlit Cloud

Add in **App Settings → Secrets**:
```toml
GROQ_API_KEY = "gsk_your_key"
```

### For Local Development

Create `.env` file:
```env
GROQ_API_KEY=gsk_your_key
```

---

## 📁 Structure

```
linkedin-post-generator/
├── app.py           # Main app
├── requirements.txt # Dependencies
├── src/            # Source code
│   ├── generator.py
│   ├── prompts.py
│   ├── database.py
│   └── utils.py
└── data/           # Database
```

---

## 🔒 Security

- ✅ Never commit `.env` file
- ✅ Use secrets management
- ✅ Rotate API keys regularly

---

## 🐛 Troubleshooting

**"Module not found":**
```bash
pip install -r requirements.txt
```

**"API key not configured":**
- Check your `.env` or Streamlit secrets
- Ensure key starts with `gsk_`

---

## 📈 API Limits (Groq Free Tier)

- **30** requests/minute
- **6,000** requests/day
- **FREE** forever

---

## 🔮 Future Features

- Image generation
- Direct LinkedIn posting
- Multi-language support
- Mobile app

---

## 🙏 Credits

- **Groq** - Ultra-fast LLM API
- **Streamlit** - Web framework
- **Meta AI** - Llama model

---

**Made with ❤️ for LinkedIn Creators**

*Deploy in 2 min • Generate in 2 sec*
