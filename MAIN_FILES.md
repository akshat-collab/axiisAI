# 📁 Main File Paths Reference

## 🎯 Quick Reference

| Purpose | Main File | Path | Command |
|---------|-----------|------|---------|
| **Streamlit Web App** | `app.py` | `axis ai/app.py` | `streamlit run app.py` |
| **Desktop App** | `Main.py` | `axis ai/Main.py` | `python Main.py` |
| **Enhanced Desktop** | `Start.py` | `axis ai/Start.py` | `python Start.py` |

## 🌐 For Streamlit Deployment

**Main File:** `app.py`

**Streamlit Cloud Configuration:**
- Main file path: `app.py`
- Requirements file: `requirements_streamlit.txt`

**Docker Configuration:**
```dockerfile
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501"]
```

## 💻 For Desktop Application

**Main File:** `Main.py` or `Start.py`

**Windows:**
```cmd
python Main.py
```

**macOS/Linux:**
```bash
python3 Main.py
```

## 📋 File Details

### `app.py` - Streamlit Web Application
- **Purpose:** Web-based AI assistant interface
- **Framework:** Streamlit
- **Port:** 8501 (default)
- **URL:** `http://localhost:8501`
- **Deployment:** Streamlit Cloud, Docker, Heroku

### `Main.py` - Desktop Application
- **Purpose:** PyQt5 desktop GUI application
- **Framework:** PyQt5
- **Features:** Full desktop interface with voice recognition
- **Platform:** Windows, macOS, Linux

### `Start.py` - Enhanced Desktop Application
- **Purpose:** Improved version of Main.py
- **Features:** Better error handling, logging, cleanup
- **Platform:** Windows, macOS, Linux

## 🚀 Quick Start Commands

### Streamlit (Web)
```bash
streamlit run app.py
```

### Desktop (Original)
```bash
python Main.py        # Windows
python3 Main.py       # Mac/Linux
```

### Desktop (Enhanced)
```bash
python Start.py       # Windows
python3 Start.py      # Mac/Linux
```

## 📍 Relative Paths

From project root (`axis ai/`):

```
.
├── app.py          ← Streamlit main file
├── Main.py         ← Desktop main file
├── Start.py        ← Enhanced desktop main file
├── Backend/        ← Backend modules
├── Frontend/       ← Frontend components
└── Data/           ← Data storage
```

## 🔧 For Deployment

### Streamlit Cloud
- **Main file:** `app.py`
- **Requirements:** `requirements_streamlit.txt`

### Docker
- **Main file:** `app.py`
- **Dockerfile:** Uses `app.py` as entry point

### Heroku
- **Main file:** `app.py`
- **Procfile:** `web: streamlit run app.py --server.port=$PORT`

---

**Summary:** Use `app.py` for web deployment, `Main.py` or `Start.py` for desktop.

