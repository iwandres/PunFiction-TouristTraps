@echo off
title PunFiction Curation Pipeline
echo ===================================================
echo   Starting PunFiction Consolidated Curation Server
echo ===================================================
echo.

if "%GEMINI_API_KEY%"=="" (
    echo WARNING: GEMINI_API_KEY environment variable is not set. 
    echo Gemini generation APIs will fail.
    echo.
    set /p GEMINI_KEY="Enter your GEMINI_API_KEY (or press Enter to run without key): "
)

if not "%GEMINI_KEY%"=="" (
    set GEMINI_API_KEY=%GEMINI_KEY%
)

echo.
echo Launching browser to http://localhost:8000 ...
start http://localhost:8000

echo.
echo Serving curation hub...
python backend/unified_server.py

pause
