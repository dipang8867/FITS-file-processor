@echo off
echo Setting up FITS File Information Extractor...

:: Create virtual environment if it doesn't exist
if not exist venv (
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Upgrade pip
python -m pip install --upgrade pip

:: Install requirements
pip install -r requirements.txt

echo.
echo Installation complete!
echo To run the FITS File Information Extractor:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the program: python fits_gui.py
pause
