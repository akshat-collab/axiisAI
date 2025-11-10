# Streamlit Cloud Setup Instructions

## ⚠️ Important: Requirements File Configuration

Streamlit Cloud is **NOT installing dependencies** because it's not detecting the requirements file correctly.

## 🔧 Solution

### Option 1: Configure Streamlit Cloud Settings (Recommended)

1. Go to your Streamlit Cloud app: https://share.streamlit.io/
2. Click on your app → **Settings** (⚙️)
3. Scroll to **"Dependencies"** section
4. Set **"Python dependencies file"** to: `requirements_streamlit.txt`
5. Click **"Save"**
6. The app will automatically redeploy

### Option 2: Rename to requirements.txt

If Option 1 doesn't work, rename the file:

```bash
git mv requirements_streamlit.txt requirements.txt
git commit -m "Rename to requirements.txt for Streamlit Cloud"
git push
```

## 📋 Current Requirements File

The requirements file `requirements_streamlit.txt` contains:

```
python-dotenv>=1.0.0
google-generativeai>=0.3.0
cohere>=4.0.0
streamlit>=1.28.0
googlesearch-python>=1.2.3
requests>=2.31.0
beautifulsoup4>=4.12.0
rich>=13.0.0
SpeechRecognition>=3.10.0
pydub>=0.25.1
mtranslate>=1.0.0
pillow>=10.0.0
edge-tts>=6.1.0
pygame>=2.5.0
```

## ✅ Verification

After configuring, check the deployment logs. You should see:

```
Installing python-dotenv...
Installing google-generativeai...
Installing cohere...
...
```

Instead of just:
```
Installing Streamlit...
```

## 🐛 Current Error

```
ModuleNotFoundError: No module named 'dotenv'
```

This happens because `python-dotenv` is not being installed. Once Streamlit Cloud is configured to use `requirements_streamlit.txt`, this will be fixed.

## 📝 Alternative: Use Streamlit Secrets

If you can't configure the requirements file, you can also use Streamlit Secrets for environment variables instead of `.env` file:

1. Go to Streamlit Cloud → Settings → Secrets
2. Add your API keys there
3. Modify `app.py` to use `st.secrets` instead of `dotenv_values`

---

**Next Step:** Configure Streamlit Cloud to use `requirements_streamlit.txt` in Settings!

