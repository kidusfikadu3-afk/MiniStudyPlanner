@echo off
TITLE ML Study Predictor (Windows)
ECHO =========================================
ECHO      ML STUDY PREDICTOR (SCIKIT-LEARN)
ECHO =========================================
ECHO.

IF EXIST "venv\" (
    ECHO [1/3] Environment found. Activating...
    call venv\Scripts\activate
) ELSE (
    ECHO [1/3] Creating Python Environment...
    python -m venv venv
    call venv\Scripts\activate
    ECHO [2/3] Installing Math Libraries...
    pip install scikit-learn pandas joblib gradio
)

ECHO [3/3] Launching GUI...
python ml_gui.py

PAUSE