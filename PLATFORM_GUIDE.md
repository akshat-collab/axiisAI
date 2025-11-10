# 🌍 Cross-Platform Guide for AXIS AI

## ✅ Platform Support

AXIS AI Streamlit app now works on:
- ✅ **Windows** (Windows 10/11)
- ✅ **macOS** (macOS 10.14+)
- ✅ **Linux** (Ubuntu, Debian, etc.)

## 🚀 Quick Start by Platform

### Windows Users

1. **Double-click** `run_streamlit.bat` OR
2. **Run in Command Prompt:**
   ```cmd
   run_streamlit.bat
   ```

### macOS/Linux Users

1. **Double-click** `run_streamlit.sh` (if allowed) OR
2. **Run in Terminal:**
   ```bash
   ./run_streamlit.sh
   ```

   If you get permission denied:
   ```bash
   chmod +x run_streamlit.sh
   ./run_streamlit.sh
   ```

## 📋 Manual Setup (All Platforms)

### Step 1: Install Python

**Windows:**
- Download from: https://www.python.org/downloads/
- Check "Add Python to PATH" during installation
- Verify: `python --version` (should show 3.9+)

**macOS:**
- Python 3.9+ is usually pre-installed
- Verify: `python3 --version`
- If not installed: `brew install python3` (requires Homebrew)

**Linux:**
- Ubuntu/Debian: `sudo apt-get install python3 python3-pip`
- Verify: `python3 --version`

### Step 2: Install Dependencies

**Windows:**
```cmd
pip install -r requirements_streamlit.txt
```

**macOS/Linux:**
```bash
pip3 install -r requirements_streamlit.txt
```

### Step 3: Configure Environment

Create a `.env` file in the project root:

```env
Username=YourName
Assistantname=Axis
GeminiAPIKey=your_gemini_api_key
CohereAPIKey=your_cohere_api_key
WeatherAPIKey=your_weather_api_key
InputLanguage=en
AssistantVoice=en-US
```

### Step 4: Run the App

**Windows:**
```cmd
streamlit run app.py
```

**macOS/Linux:**
```bash
streamlit run app.py
```

Or use the platform-specific scripts:
- Windows: `run_streamlit.bat`
- macOS/Linux: `./run_streamlit.sh`

## 🔧 Platform-Specific Notes

### Windows

- **Path Separators:** All paths now use `os.path.join()` for compatibility
- **File Permissions:** May need to run as Administrator for some operations
- **Firewall:** Windows Firewall may ask for permission on first run

### macOS

- **Python Version:** Use `python3` command (not `python`)
- **Permissions:** May need to grant Terminal full disk access
- **Security:** macOS Gatekeeper may require approval for scripts

### Linux

- **Dependencies:** May need to install system packages:
  ```bash
  sudo apt-get install python3-dev python3-pip
  ```
- **Permissions:** Use `chmod +x` for shell scripts
- **Audio:** May need `alsa-utils` for audio features:
  ```bash
  sudo apt-get install alsa-utils
  ```

## 🐛 Troubleshooting

### Common Issues

#### "Python not found"
- **Windows:** Add Python to PATH or use full path: `C:\Python39\python.exe`
- **macOS/Linux:** Use `python3` instead of `python`

#### "Permission denied" (macOS/Linux)
```bash
chmod +x run_streamlit.sh
```

#### "Module not found"
```bash
# Windows
pip install -r requirements_streamlit.txt

# macOS/Linux
pip3 install -r requirements_streamlit.txt
```

#### "Port already in use"
```bash
streamlit run app.py --server.port=8502
```

### Platform-Specific Fixes

#### Windows
- If `pip` doesn't work, try: `python -m pip install ...`
- Use Command Prompt (cmd) or PowerShell
- Avoid using Git Bash for running scripts

#### macOS
- If `pip3` fails, try: `python3 -m pip install ...`
- May need to use `sudo` for system-wide installs (not recommended)
- Use Terminal.app or iTerm2

#### Linux
- Use `sudo` only if installing system-wide packages
- Prefer user installation: `pip3 install --user ...`
- Check Python version: `python3 --version`

## 📁 Directory Structure

All platforms use the same structure:
```
axis ai/
├── app.py                    # Main Streamlit app
├── Backend/                   # Backend modules
├── Data/                      # Data storage (auto-created)
├── Frontend/
│   └── Files/                 # Temp files (auto-created)
├── .env                       # Environment variables
├── requirements_streamlit.txt # Dependencies
├── run_streamlit.bat          # Windows launcher
└── run_streamlit.sh           # macOS/Linux launcher
```

## 🔒 Security Notes

- Never commit `.env` file to Git
- Use environment variables for sensitive data
- Keep API keys secure
- Review file permissions on shared systems

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Installation Guide](https://www.python.org/downloads/)
- [Cross-Platform Python Guide](https://docs.python.org/3/library/os.path.html)

## ✅ Verification Checklist

Before running, ensure:
- [ ] Python 3.9+ is installed
- [ ] Dependencies are installed (`pip install -r requirements_streamlit.txt`)
- [ ] `.env` file exists with API keys
- [ ] `Data` directory exists (auto-created)
- [ ] `Frontend/Files` directory exists (auto-created)
- [ ] Port 8501 is available (or use `--server.port`)

## 🎯 Next Steps

1. ✅ Verify Python installation
2. ✅ Install dependencies
3. ✅ Configure `.env` file
4. ✅ Run the app
5. ✅ Access at `http://localhost:8501`

---

**Your AXIS AI is now cross-platform ready! 🚀**

