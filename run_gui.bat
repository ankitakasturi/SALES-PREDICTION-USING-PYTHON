@echo off
title Sales Prediction System

REM Ensure we run from the script directory so gui_app.py is found
cd /d "%~dp0"

REM Try `python`, then `py -3`, then the known full path. Provide guidance if none found.
where python >nul 2>&1
if %ERRORLEVEL%==0 (
	echo Using python from PATH
	python gui_app.py
	pause
	exit /b
)

py -3 --version >nul 2>&1
if %ERRORLEVEL%==0 (
	echo Using py launcher
	py -3 gui_app.py
	pause
	exit /b
)

if exist "C:\Users\hp\AppData\Local\Programs\Python\Python313\python.exe" (
	echo Using Python at C:\Users\hp\AppData\Local\Programs\Python\Python313\python.exe
	"C:\Users\hp\AppData\Local\Programs\Python\Python313\python.exe" gui_app.py
	pause
	exit /b
)

echo.
echo Python interpreter not found.
echo - Install Python from https://www.python.org/downloads/ and enable "Add Python to PATH" during install.
echo - Or disable the Microsoft Store app execution alias: Settings → Apps → Advanced app settings → App execution aliases.
echo - After installing, reopen the terminal and run this script again.
echo.
pause
