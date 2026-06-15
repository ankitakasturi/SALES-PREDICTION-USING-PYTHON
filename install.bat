@echo off
REM Sales Prediction System - Quick Start Script for Windows

echo.
echo ========================================================
echo Sales Prediction Using Machine Learning
echo ========================================================
echo.

echo Step 1: Installing required packages...
echo.
pip install -r requirements.txt

echo.
echo Step 2: Generating initial data...
echo.
python -c "from data_handler import generate_sales_data; data=generate_sales_data(); print('✓ Data generated successfully'); print('  Records:', len(data)); print('  Features:', list(data.columns))"

echo.
echo Step 3: Training sample models...
echo.
python models.py

echo.
echo ========================================================
echo Installation Complete!
echo ========================================================
echo.
echo Next Steps:
echo  1. Run GUI Application:
echo     python gui_app.py
echo.
echo  2. Or run Jupyter Notebook:
echo     jupyter notebook comprehensive_sales_prediction.ipynb
echo.
echo ========================================================
echo.
pause
