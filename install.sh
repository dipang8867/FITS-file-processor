#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Make the GUI script executable
chmod +x fits_gui.py

echo "Installation complete!"
echo "To run the FITS File Information Extractor:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the program: python fits_gui.py"
