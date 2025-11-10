# AXIS AI - Advanced AI Assistant

🤖 **AXIS AI** is an advanced AI assistant powered by Gemini and Cohere, featuring voice recognition, real-time search, and intelligent automation.

## 🌟 Features

- 💬 **Intelligent Chatbot** - Powered by Google Gemini AI
- 🔍 **Real-time Search** - Get up-to-date information from the web
- 🎤 **Voice Recognition** - Speech-to-text input support
- 🎨 **Image Generation** - AI-powered image creation
- 🤖 **Decision Making Model** - Smart task routing using Cohere
- 🌐 **Web Deployment** - Streamlit-based web interface
- 💻 **Cross-Platform** - Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Streamlit Web App (Recommended)

**Windows:**
```cmd
run_streamlit.bat
```

**macOS/Linux:**
```bash
./run_streamlit.sh
```

**Manual:**
```bash
pip install -r requirements_streamlit.txt
streamlit run app.py
```

### Desktop Application

**Windows:**
```cmd
python Main.py
```

**macOS/Linux:**
```bash
python3 Main.py
```

## 📋 Requirements

- Python 3.9+
- API Keys:
  - Gemini API Key (from Google AI Studio)
  - Cohere API Key (from Cohere Dashboard)
  - Weather API Key (optional, from OpenWeatherMap)

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
Username=YourName
Assistantname=Axis
GeminiAPIKey=your_gemini_api_key
CohereAPIKey=your_cohere_api_key
WeatherAPIKey=your_weather_api_key
InputLanguage=en
AssistantVoice=en-US
```

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/akshat-collab/axiisAI.git
   cd axiisAI
   ```

2. **Install dependencies:**
   ```bash
   # For Streamlit app
   pip install -r requirements_streamlit.txt
   
   # For desktop app
   pip install -r Requirements.txt
   ```

3. **Configure environment:**
   - Copy `.env.example` to `.env` (if available)
   - Add your API keys

4. **Run the application:**
   ```bash
   streamlit run app.py  # Web version
   # OR
   python Main.py       # Desktop version
   ```

## 🌍 Platform Support

- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu/Debian)

See [PLATFORM_GUIDE.md](PLATFORM_GUIDE.md) for platform-specific instructions.

## 📚 Documentation

- [Streamlit Deployment Guide](README_STREAMLIT.md)
- [Platform Guide](PLATFORM_GUIDE.md)
- [Cross-Platform Summary](CROSS_PLATFORM_SUMMARY.md)
- [Deployment Summary](DEPLOYMENT_SUMMARY.md)

## 🏗️ Project Structure

```
axiisAI/
├── app.py                    # Streamlit web application
├── Main.py                    # Desktop application entry point
├── Start.py                   # Enhanced startup script
├── Backend/                   # Core AI modules
│   ├── Chatbot.py            # Gemini chatbot integration
│   ├── Model.py              # Cohere DMM
│   ├── RealtimeSearchEngine.py
│   ├── Automation.py
│   ├── SpeechToText.py
│   └── TextToSpeech.py
├── Frontend/                  # UI components
│   ├── GUI.py                # PyQt5 desktop GUI
│   └── Graphics/             # UI assets
├── Data/                      # Data storage
├── requirements_streamlit.txt # Streamlit dependencies
├── Requirements.txt          # Desktop app dependencies
└── .env                      # Environment variables (create this)
```

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy!

See [README_STREAMLIT.md](README_STREAMLIT.md) for detailed instructions.

### Docker

```bash
docker build -t axis-ai .
docker run -p 8501:8501 axis-ai
```

## 🔧 Technologies Used

- **AI Models:**
  - Google Gemini Pro (Chatbot)
  - Cohere (Decision Making Model)
  
- **Frameworks:**
  - Streamlit (Web UI)
  - PyQt5 (Desktop UI)
  
- **Libraries:**
  - SpeechRecognition
  - Edge TTS
  - BeautifulSoup4
  - Selenium

## 📝 License

This project is part of AXIS AI Assistant.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ by the AXIS AI Team**

