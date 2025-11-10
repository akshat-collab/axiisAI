# 🚨 CRITICAL FIX: Streamlit Cloud Running Wrong File

## ❌ Current Error

Streamlit Cloud is trying to run `Main.py` instead of `app.py`:

```
File "/mount/src/axiisai/Main.py", line 1, in <module>
    from Frontend.GUI import (
    from PyQt5.QtWidgets import ...
```

**Problem:** `Main.py` is for desktop (PyQt5), not web (Streamlit)!

## ✅ Solution: Change Main File in Streamlit Cloud

### Step 1: Go to Streamlit Cloud Settings

1. Go to: https://share.streamlit.io/
2. Click on your app
3. Click **"⚙️ Settings"** (top right or "Manage app" → Settings)

### Step 2: Change Main File

1. Scroll to **"General settings"** section
2. Find **"Main file path"** field
3. Change from: `Main.py`
4. Change to: `app.py`
5. Click **"Save"**

### Step 3: Verify Requirements File

While you're in Settings:
1. Scroll to **"Dependencies"** section
2. Set **"Python dependencies file"** to: `requirements_streamlit.txt`
3. Click **"Save"**

### Step 4: Redeploy

The app will automatically redeploy. Wait for it to finish.

## 📋 Correct Configuration

- **Main file:** `app.py` ✅
- **Requirements file:** `requirements_streamlit.txt` ✅

## 🔍 How to Verify

After changing settings, check the deployment logs. You should see:

```
🚀 Starting up repository: 'axiisai', branch: 'main', main module: 'app.py'
```

NOT:
```
main module: 'Main.py'  ❌
```

## ⚠️ Why This Happened

Streamlit Cloud auto-detected `Main.py` as the main file because:
- It's named "Main.py" (common pattern)
- It might have been the first Python file detected
- Or it was manually set incorrectly

## ✅ After Fix

Once configured correctly:
- ✅ `app.py` will run (Streamlit web app)
- ✅ All dependencies will install
- ✅ No PyQt5 errors
- ✅ App will work!

---

**ACTION REQUIRED:** Change main file from `Main.py` to `app.py` in Streamlit Cloud Settings!

