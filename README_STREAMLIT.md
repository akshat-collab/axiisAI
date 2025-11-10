# AXIS AI - Streamlit Deployment Guide

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory with:
   ```
   Username=YourName
   Assistantname=Axis
   GeminiAPIKey=your_gemini_api_key
   CohereAPIKey=your_cohere_api_key
   WeatherAPIKey=your_weather_api_key
   InputLanguage=en
   AssistantVoice=en-US
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

4. **Access the app:**
   Open your browser to `http://localhost:8501`

## 📦 Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/axis-ai.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Set requirements file: `requirements_streamlit.txt`
   - Add your secrets (API keys) in the Secrets section
   - Click "Deploy"

3. **Configure Secrets:**
   In Streamlit Cloud, go to Settings → Secrets and add:
   ```toml
   Username = "YourName"
   Assistantname = "Axis"
   GeminiAPIKey = "your_gemini_api_key"
   CohereAPIKey = "your_cohere_api_key"
   WeatherAPIKey = "your_weather_api_key"
   InputLanguage = "en"
   AssistantVoice = "en-US"
   ```

### Option 2: Docker Deployment

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements_streamlit.txt .
   RUN pip install --no-cache-dir -r requirements_streamlit.txt

   COPY . .

   EXPOSE 8501

   HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

   ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and run:**
   ```bash
   docker build -t axis-ai .
   docker run -p 8501:8501 -e GEMINI_API_KEY=your_key axis-ai
   ```

### Option 3: Heroku

1. **Create Procfile:**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create setup.sh:**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   " > ~/.streamlit/config.toml
   ```

3. **Deploy:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## 🔧 Configuration

### Environment Variables

The app uses `.env` file for local development. For production, use:
- Streamlit Cloud: Secrets section
- Docker: Environment variables
- Heroku: Config vars

### Required API Keys

1. **Gemini API Key:**
   - Get from: https://makersuite.google.com/app/apikey
   - Used for: Chatbot and AI responses

2. **Cohere API Key:**
   - Get from: https://dashboard.cohere.com/
   - Used for: Decision Making Model (DMM)

3. **Weather API Key (Optional):**
   - Get from: https://openweathermap.org/api
   - Used for: Weather queries

## 📝 Features

- ✅ Chat interface with message history
- ✅ Voice input support (audio file upload)
- ✅ Real-time search integration
- ✅ AI-powered responses using Gemini
- ✅ Decision Making Model (DMM) using Cohere
- ✅ Chat history persistence
- ✅ Export chat history
- ✅ Dark theme UI

## 🐛 Troubleshooting

### Common Issues

1. **Module not found errors:**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **API key errors:**
   - Check your `.env` file or Streamlit Secrets
   - Ensure all required keys are set

3. **Port already in use:**
   ```bash
   streamlit run app.py --server.port=8502
   ```

4. **Speech recognition not working:**
   - Install: `pip install SpeechRecognition pydub`
   - For Google recognition, ensure internet connection

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Cloud](https://streamlit.io/cloud)
- [Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)

## 🔒 Security Notes

- Never commit `.env` file to Git
- Use Streamlit Secrets for production
- Keep API keys secure
- Use environment variables in production

## 📄 License

This project is part of AXIS AI Assistant.

